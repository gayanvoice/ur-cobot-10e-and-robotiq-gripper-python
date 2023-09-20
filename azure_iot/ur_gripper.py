import asyncio
import json
import math
import xml.etree.ElementTree as ET
import URBasic
from azure_iot.Device import Device
from model.configuration.shared_iot_configuration_model import SharedIotConfigurationModel
from model.configuration.ur_gripper_iot_configuration_model import URGripperIotConfigurationModel
from URGripper.ur_gripper_controller import URGripperController
from model.gripper_command_model import GripperCommandModel
from model.joint_position_model import JointPositionModel
from model.move_j_command_model import MoveJCommandModel
from model.response.activate_gripper_command_response_model import ActivateGripperCommandResponseModel
from model.response.close_gripper_command_response_model import CloseGripperCommandResponseModel
from model.response.close_popup_command_response_model import ClosePopupCommandResponseModel
from model.response.close_safety_popup_command_response_model import CloseSafetyPopupCommandResponseModel
from model.response.move_j_command_response_model import MoveJCommandResponseModel
from model.response.open_gripper_command_response_model import OpenGripperCommandResponseModel
from model.response.open_popup_command_response_model import OpenPopupCommandResponseModel
from model.response.pause_command_response_model import PauseCommandResponseModel
from model.response.play_command_response_model import PlayCommandResponseModel
from model.response.power_off_command_response_model import PowerOffCommandResponseModel
from model.response.power_on_command_response_model import PowerOnCommandResponseModel
from model.response.unlock_protective_stop_command_response_model import UnlockProtectiveStopCommandResponseModel


class URGripper:

    def __init__(self):
        self.device = None
        self.ur_gripper_controller = None

    @staticmethod
    def stdin_listener():
        while True:
            selection = input("Press Q to quit Ur Gripper IoT Application\n")
            if selection == "Q" or selection == "q":
                break

    async def connect_ur_gripper_physical_device(self, ur_gripper_iot_configuration_model):
        self.ur_gripper_controller = URGripperController()
        self.ur_gripper_controller.connect(
            hostname=ur_gripper_iot_configuration_model.host,
            port=ur_gripper_iot_configuration_model.port,
            socket_timeout=ur_gripper_iot_configuration_model.socket_timeout)
        self.ur_gripper_controller.activate()

    async def connect_ur_gripper_iot_device(self, ur_gripper_iot_configuration_model):
        self.device = Device(model_id=ur_gripper_iot_configuration_model.model_id,
                             provisioning_host=ur_gripper_iot_configuration_model.provisioning_host,
                             id_scope=ur_gripper_iot_configuration_model.id_scope,
                             registration_id=ur_gripper_iot_configuration_model.registration_id,
                             symmetric_key=ur_gripper_iot_configuration_model.symmetric_key)
        await self.device.create_iot_hub_device_client()
        await self.device.iot_hub_device_client.connect()

    async def connect_azure_iot(self, queue):
        iot_configuration_xml_file_path = "configuration/iot_configuration.xml"

        shared_iot_configuration_model = SharedIotConfigurationModel().get(
            iot_configuration_xml_file_path=iot_configuration_xml_file_path)
        ur_gripper_iot_configuration_model = URGripperIotConfigurationModel().get(
            iot_configuration_xml_file_path=iot_configuration_xml_file_path)

        await self.connect_ur_gripper_iot_device(ur_gripper_iot_configuration_model=ur_gripper_iot_configuration_model)
        await self.connect_ur_gripper_physical_device(
            ur_gripper_iot_configuration_model=ur_gripper_iot_configuration_model)

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

        send_telemetry_task = asyncio.ensure_future(self.send_telemetry_task(
            shared_iot_configuration_model=shared_iot_configuration_model))

        loop = asyncio.get_running_loop()
        user_finished = loop.run_in_executor(None, self.stdin_listener)

        await user_finished

        if not command_listeners.done():
            result = {'Status': 'Done'}
            command_listeners.set_result(result)

        self.ur_gripper_controller.disconnect()
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
            self.ur_gripper_controller.open_gripper()
            return activate_gripper_command_response_model.get_successfully_executed()
        except Exception as ex:
            return activate_gripper_command_response_model.get_exception(str(ex))

    async def open_gripper_command_request_handler(self):
        open_gripper_command_response_model = OpenGripperCommandResponseModel()
        try:
            self.ur_gripper_controller.open_gripper()
            return open_gripper_command_response_model.get_successfully_executed()
        except Exception as ex:
            return open_gripper_command_response_model.get_exception(str(ex))

    async def close_gripper_command_request_handler(self):
        close_gripper_command_response_model = CloseGripperCommandResponseModel()
        try:
            self.ur_gripper_controller.close_gripper()
            return close_gripper_command_response_model.get_successfully_executed()
        except Exception as ex:
            return close_gripper_command_response_model.get_exception(str(ex))

    async def send_telemetry_task(self, shared_iot_configuration_model):
        while True:
            try:
                telemetry = {
                    "act": self.ur_gripper_controller.get_activate(),
                    "gto": self.ur_gripper_controller.get_goto(),
                    "for": self.ur_gripper_controller.get_force(),
                    "spe": self.ur_gripper_controller.get_speed(),
                    "pos": self.ur_gripper_controller.get_position(),
                    "sta": self.ur_gripper_controller.get_status(),
                    "pre": self.ur_gripper_controller.get_position_request(),
                    "obj": self.ur_gripper_controller.get_object_detection(),
                    "flt": self.ur_gripper_controller.get_fault(),
                }
                print(json.dumps(telemetry, default=lambda o: o.__dict__, indent=1))
                await self.device.send_telemetry(telemetry=telemetry)
            except Exception as ex:
                print(ex)
            await asyncio.sleep(shared_iot_configuration_model.telemetry_delay)
