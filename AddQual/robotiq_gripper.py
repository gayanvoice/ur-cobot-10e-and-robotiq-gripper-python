import asyncio
import json
import logging
import random
import time

from AddQual import addqual_global
from AddQual.Device import Device
from model.configuration.shared_iot_configuration_model import SharedIotConfigurationModel
from model.configuration.robotiq_gripper_iot_configuration import RobotiqGripperIotConfigurationModel
from RobotiqGripper.robotiq_gripper_controller import RobotiqGripperController
from model.response.activate_gripper_command_response_model import ActivateGripperCommandResponseModel
from model.response.close_gripper_command_response_model import CloseGripperCommandResponseModel
from model.response.open_gripper_command_response_model import OpenGripperCommandResponseModel


class RobotiqGripper:

    def __init__(self):
        self.device = None
        self.robotiq_gripper_controller = None

    @staticmethod
    def stdin_listener():
        while True:
            if addqual_global.is_queue_running is False:
                break

    async def connect_ur_gripper_physical_device(self, robotiq_gripper_iot_configuration_model):
        self.robotiq_gripper_controller = RobotiqGripperController()
        self.robotiq_gripper_controller.connect(
            hostname=robotiq_gripper_iot_configuration_model.host,
            port=robotiq_gripper_iot_configuration_model.port,
            socket_timeout=robotiq_gripper_iot_configuration_model.socket_timeout)
        self.robotiq_gripper_controller.activate()

    async def connect_ur_gripper_iot_device(self, robotiq_gripper_iot_configuration_model):
        self.device = Device(model_id=robotiq_gripper_iot_configuration_model.model_id,
                             provisioning_host=robotiq_gripper_iot_configuration_model.provisioning_host,
                             id_scope=robotiq_gripper_iot_configuration_model.id_scope,
                             registration_id=robotiq_gripper_iot_configuration_model.registration_id,
                             symmetric_key=robotiq_gripper_iot_configuration_model.symmetric_key)
        await self.device.create_iot_hub_device_client()
        await self.device.iot_hub_device_client.connect()

    async def connect_azure_iot(self, queue):
        iot_configuration_xml_file_path = "configuration/iot_configuration.xml"

        shared_iot_configuration_model = SharedIotConfigurationModel().get(
            iot_configuration_xml_file_path=iot_configuration_xml_file_path)
        robotiq_gripper_iot_configuration_model = RobotiqGripperIotConfigurationModel().get(
            iot_configuration_xml_file_path=iot_configuration_xml_file_path)

        await self.connect_ur_gripper_iot_device(
            robotiq_gripper_iot_configuration_model=robotiq_gripper_iot_configuration_model)

        if addqual_global.is_dev_mode is False:
            await self.connect_ur_gripper_physical_device(
                robotiq_gripper_iot_configuration_model=robotiq_gripper_iot_configuration_model)

        command_listeners = asyncio.gather(
            self.device.execute_command_listener(
                method_name="OpenGripperCommand",
                request_handler=self.open_gripper_command_request_handler,
                response_handler=self.command_response_handler,
            ),
            self.device.execute_command_listener(
                method_name="CloseGripperCommand",
                request_handler=self.close_gripper_command_request_handler,
                response_handler=self.command_response_handler,
            ),
            self.device.execute_command_listener(
                method_name="ActivateGripperCommand",
                request_handler=self.activate_gripper_command_request_handler,
                response_handler=self.command_response_handler,
            ),
        )

        if addqual_global.is_dev_mode:
            send_telemetry_task = asyncio.ensure_future(self.send_telemetry_development_task(
                shared_iot_configuration_model=shared_iot_configuration_model))
        else:
            send_telemetry_task = asyncio.ensure_future(self.send_telemetry_production_task(
                shared_iot_configuration_model=shared_iot_configuration_model))

        loop = asyncio.get_running_loop()
        user_finished = loop.run_in_executor(None, self.stdin_listener)
        await user_finished

        if not command_listeners.done():
            result = {'Status': 'Done'}
            command_listeners.set_result(list(result.values()))

        if addqual_global.is_dev_mode is False:
            self.robotiq_gripper_controller.disconnect()
        command_listeners.cancel()

        send_telemetry_task.cancel()

        await self.device.iot_hub_device_client.shutdown()
        await queue.put(None)

    @staticmethod
    def command_response_handler(command_response_model):
        return json.dumps(command_response_model, default=lambda o: o.__dict__, indent=1)

    async def activate_gripper_command_request_handler(self):
        activate_gripper_command_response_model = ActivateGripperCommandResponseModel()
        try:
            if addqual_global.is_dev_mode:
                time.sleep(1)
            else:
                self.robotiq_gripper_controller.activate()
            return activate_gripper_command_response_model.get_successfully_executed()
        except Exception as ex:
            return activate_gripper_command_response_model.get_exception(str(ex))

    async def open_gripper_command_request_handler(self):
        open_gripper_command_response_model = OpenGripperCommandResponseModel()
        try:
            if addqual_global.is_dev_mode:
                time.sleep(1)
            else:
                self.robotiq_gripper_controller.open_gripper()
            return open_gripper_command_response_model.get_successfully_executed()
        except Exception as ex:
            return open_gripper_command_response_model.get_exception(str(ex))

    async def close_gripper_command_request_handler(self):
        close_gripper_command_response_model = CloseGripperCommandResponseModel()
        try:
            if addqual_global.is_dev_mode:
                time.sleep(1)
            else:
                self.robotiq_gripper_controller.close_gripper()
            return close_gripper_command_response_model.get_successfully_executed()
        except Exception as ex:
            return close_gripper_command_response_model.get_exception(str(ex))

    async def send_telemetry_production_task(self, shared_iot_configuration_model):
        while True:
            try:
                telemetry = {
                    "act": self.robotiq_gripper_controller.get_activate(),
                    "gto": self.robotiq_gripper_controller.get_goto(),
                    "for": self.robotiq_gripper_controller.get_force(),
                    "spe": self.robotiq_gripper_controller.get_speed(),
                    "pos": self.robotiq_gripper_controller.get_position(),
                    "sta": self.robotiq_gripper_controller.get_status(),
                    "pre": self.robotiq_gripper_controller.get_position_request(),
                    "obj": self.robotiq_gripper_controller.get_object_detection(),
                    "flt": self.robotiq_gripper_controller.get_fault(),
                }
                logging.info(json.dumps(telemetry, default=lambda o: o.__dict__, indent=1))
                await self.device.send_telemetry(telemetry=telemetry)
            except Exception as ex:
                logging.error(ex)
            await asyncio.sleep(shared_iot_configuration_model.telemetry_delay)

    async def send_telemetry_development_task(self, shared_iot_configuration_model):
        while True:
            try:
                act = random.randint(0, 1)
                gto = random.randint(0, 1)
                force = random.randint(10, 100)
                spe = random.randint(10, 100)
                pos = random.randint(3, 227)
                sta = random.randint(0, 3)
                pre = random.randint(3, 227)
                obj = random.randint(0, 3)
                flt = random.randint(0, 15)
                telemetry = {
                    "act": act,
                    "gto": gto,
                    "for": force,
                    "spe": spe,
                    "pos": pos,
                    "sta": sta,
                    "pre": pre,
                    "obj": obj,
                    "flt": flt,
                }
                logging.info(json.dumps(telemetry, default=lambda o: o.__dict__, indent=1))
                await self.device.send_telemetry(telemetry=telemetry)
            except Exception as ex:
                logging.error(ex)
            await asyncio.sleep(shared_iot_configuration_model.telemetry_delay)
