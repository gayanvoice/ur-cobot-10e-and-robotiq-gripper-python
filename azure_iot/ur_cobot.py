import asyncio
import json
import math
import xml.etree.ElementTree as ET
import URBasic
from azure_iot.Device import Device
from model.configuration.shared_iot_configuration_model import SharedIotConfigurationModel
from model.configuration.ur_cobot_iot_configuration_model import URCobotIotConfigurationModel
from model.gripper_command_model import GripperCommandModel
from model.joint_position_model import JointPositionModel
from model.move_j_command_model import MoveJCommandModel
from model.response.close_popup_command_response_model import ClosePopupCommandResponseModel
from model.response.close_safety_popup_command_response_model import CloseSafetyPopupCommandResponseModel
from model.response.move_j_command_response_model import MoveJCommandResponseModel
from model.response.open_popup_command_response_model import OpenPopupCommandResponseModel
from model.response.pause_command_response_model import PauseCommandResponseModel
from model.response.play_command_response_model import PlayCommandResponseModel
from model.response.power_off_command_response_model import PowerOffCommandResponseModel
from model.response.power_on_command_response_model import PowerOnCommandResponseModel
from model.response.unlock_protective_stop_command_response_model import UnlockProtectiveStopCommandResponseModel


class URCobot:

    def __init__(self):
        self.device = None
        self.ur_script_ext = None

    @staticmethod
    def stdin_listener():
        while True:
            selection = input("Press Q to quit Cobot IoT Application\n")
            if selection == "Q" or selection == "q":
                break

    async def connect_ur_cobot_physical_device(self, ur_cobot_iot_configuration_model):
        robot_model = URBasic.robotModel.RobotModel()
        self.ur_script_ext = URBasic.urScriptExt.UrScriptExt(
            host=ur_cobot_iot_configuration_model.host,
            robotModel=robot_model)
        self.ur_script_ext.reset_error()

    async def connect_ur_cobot_iot_device(self, ur_cobot_iot_configuration_model):
        self.device = Device(model_id=ur_cobot_iot_configuration_model.model_id,
                             provisioning_host=ur_cobot_iot_configuration_model.provisioning_host,
                             id_scope=ur_cobot_iot_configuration_model.id_scope,
                             registration_id=ur_cobot_iot_configuration_model.registration_id,
                             symmetric_key=ur_cobot_iot_configuration_model.symmetric_key)
        await self.device.create_iot_hub_device_client()
        await self.device.iot_hub_device_client.connect()

    async def connect_azure_iot(self, queue):
        iot_configuration_xml_file_path = "configuration/iot_configuration.xml"

        shared_iot_configuration_model = SharedIotConfigurationModel().get(
            iot_configuration_xml_file_path=iot_configuration_xml_file_path)
        ur_cobot_iot_configuration_model = URCobotIotConfigurationModel().get(
            iot_configuration_xml_file_path=iot_configuration_xml_file_path)

        await self.connect_ur_cobot_iot_device(
            ur_cobot_iot_configuration_model=ur_cobot_iot_configuration_model)
        await self.connect_ur_cobot_physical_device(
            ur_cobot_iot_configuration_model=ur_cobot_iot_configuration_model)

        command_listeners = asyncio.gather(
            self.device.execute_command_listener(
                method_name="MoveJCommand",
                request_handler=self.move_j_command_request_handler,
                response_handler=self.command_response_handler,
            ),
            self.device.execute_command_listener(
                method_name="PauseCommand",
                request_handler=self.pause_command_request_handler,
                response_handler=self.command_response_handler,
            ),
            self.device.execute_command_listener(
                method_name="PlayCommand",
                request_handler=self.play_command_request_handler,
                response_handler=self.command_response_handler,
            ),
            self.device.execute_command_listener(
                method_name="CloseSafetyPopupCommand",
                request_handler=self.close_safety_popup_command_request_handler,
                response_handler=self.command_response_handler,
            ),
            self.device.execute_command_listener(
                method_name="UnlockProtectiveStopCommand",
                request_handler=self.unlock_protective_stop_command_request_handler,
                response_handler=self.command_response_handler,
            ),
            self.device.execute_command_listener(
                method_name="OpenPopupCommand",
                request_handler=self.open_popup_command_request_handler,
                response_handler=self.command_response_handler,
            ),
            self.device.execute_command_listener(
                method_name="ClosePopupCommand",
                request_handler=self.close_popup_command_request_handler,
                response_handler=self.command_response_handler,
            ),
            self.device.execute_command_listener(
                method_name="PowerOnCommand",
                request_handler=self.power_on_command_request_handler,
                response_handler=self.command_response_handler,
            ),
            self.device.execute_command_listener(
                method_name="PowerOffPopupCommand",
                request_handler=self.power_off_command_request_handler,
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

        self.ur_script_ext.close()
        command_listeners.cancel()

        send_telemetry_task.cancel()

        await self.device.iot_hub_device_client.shutdown()
        await queue.put(None)

    async def move_j_command_request_handler(self, request_payload):
        command_response_model = MoveJCommandResponseModel()
        try:
            move_j_command_model = MoveJCommandModel.get_move_j_command_model_using_request_payload(request_payload)
            # move_j_command_model.validate()
            for joint_position_model in move_j_command_model.joint_position_model_array:
                joint_position_array = JointPositionModel.get_position_array_from_joint_position_model(
                    joint_position_model=joint_position_model
                )
                self.ur_script_ext.movej(q=joint_position_array,
                                         a=move_j_command_model.acceleration,
                                         v=move_j_command_model.velocity,
                                         t=move_j_command_model.time_s,
                                         r=move_j_command_model.blend_radius)
            return command_response_model.get_successfully_executed()
        except Exception as ex:
            return command_response_model.get_exception(str(ex))

    @staticmethod
    def command_response_handler(command_response_model):
        return json.dumps(command_response_model, default=lambda o: o.__dict__, indent=1)

    async def pause_command_request_handler(self, request_payload):
        command_response_model = PauseCommandResponseModel()
        try:
            self.ur_script_ext.pause()
            return command_response_model.get_successfully_executed()
        except Exception as ex:
            return command_response_model.get_exception(str(ex))

    async def play_command_request_handler(self, request_payload):
        command_response_model = PlayCommandResponseModel()
        try:
            self.ur_script_ext.play()
            return command_response_model.get_successfully_executed()
        except Exception as ex:
            return command_response_model.get_exception(str(ex))

    async def close_safety_popup_command_request_handler(self, request_payload):
        command_response_model = CloseSafetyPopupCommandResponseModel()
        try:
            self.ur_script_ext.close_safety_popup()
            return command_response_model.get_successfully_executed()
        except Exception as ex:
            return command_response_model.get_exception(str(ex))

    async def unlock_protective_stop_command_request_handler(self, request_payload):
        command_response_model = UnlockProtectiveStopCommandResponseModel()
        try:
            self.ur_script_ext.unlock_protective_stop()
            return command_response_model.get_successfully_executed()
        except Exception as ex:
            return command_response_model.get_exception(str(ex))

    async def open_popup_command_request_handler(self, request_payload):
        command_response_model = OpenPopupCommandResponseModel()
        try:
            self.ur_script_ext.open_popup(popup_text=request_payload)
            return command_response_model.get_successfully_executed()
        except Exception as ex:
            return command_response_model.get_exception(str(ex))

    async def close_popup_command_request_handler(self, request_payload):
        command_response_model = ClosePopupCommandResponseModel()
        try:
            self.ur_script_ext.close_popup()
            return command_response_model.get_successfully_executed()
        except Exception as ex:
            return command_response_model.get_exception(str(ex))

    async def power_on_command_request_handler(self, request_payload):
        command_response_model = PowerOnCommandResponseModel()
        try:
            self.ur_script_ext.power_on()
            return command_response_model.get_successfully_executed()
        except Exception as ex:
            return command_response_model.get_exception(str(ex))

    async def power_off_command_request_handler(self, request_payload):
        command_response_model = PowerOffCommandResponseModel()
        try:
            self.ur_script_ext.power_off()
            return command_response_model.get_successfully_executed()
        except Exception as ex:
            return command_response_model.get_exception(str(ex))

    async def send_telemetry_task(self, shared_iot_configuration_model):
        while True:
            try:
                telemetry = {
                    "target_q": self.ur_script_ext.get_target_q(),
                    "target_qd": self.ur_script_ext.get_target_qd(),
                    "target_qdd": self.ur_script_ext.get_target_qdd(),
                    "target_current": self.ur_script_ext.get_target_current(),
                    "target_moment": self.ur_script_ext.get_target_moment(),
                    "actual_current": self.ur_script_ext.get_actual_current(),
                    "actual_q": self.ur_script_ext.get_actual_q(),
                    "actual_qd": self.ur_script_ext.get_actual_qd(),
                    "joint_control_output": self.ur_script_ext.get_joint_control_output(),
                    "actual_TCP_force": self.ur_script_ext.get_actual_tcp_force(),
                    "joint_temperatures": self.ur_script_ext.get_joint_temperatures(),
                    "joint_mode": self.ur_script_ext.get_joint_mode(),
                    "actual_tool_accelerometer": self.ur_script_ext.get_actual_tool_accelerometer(),
                    "speed_scaling": self.ur_script_ext.get_speed_scaling(),
                    "actual_momentum": self.ur_script_ext.get_actual_momentum(),
                    "actual_main_voltage": self.ur_script_ext.get_actual_main_voltage(),
                    "actual_robot_voltage": self.ur_script_ext.get_actual_robot_voltage(),
                    "actual_robot_current": self.ur_script_ext.get_actual_robot_current(),
                    "actual_joint_voltage": self.ur_script_ext.get_actual_joint_voltage(),
                    "runtime_state": self.ur_script_ext.get_run_time_state(),
                    "robot_mode": self.ur_script_ext.get_robot_mode(),
                    "safety_mode": self.ur_script_ext.get_safety_mode(),
                    "analog_io_types": self.ur_script_ext.get_analog_io_types(),
                    "io_current": self.ur_script_ext.get_io_current(),
                    "tool_mode": self.ur_script_ext.get_tool_mode(),
                    "tool_output_voltage": self.ur_script_ext.get_tool_output_voltage(),
                    "tool_output_current": self.ur_script_ext.get_tool_output_current(),
                }
                print([math.degrees(value) for value in self.ur_script_ext.get_actual_q()])
                await self.device.send_telemetry(telemetry=telemetry)
            except Exception as ex:
                print(ex)
            await asyncio.sleep(shared_iot_configuration_model.telemetry_delay)
