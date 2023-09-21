import json
import time
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod

import urx
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper

# from URGripper.ur_gripper import UrGripper
# from azure_iot.URGripper import URGripper
# from URGripper.cmodel_urcap import RobotiqCModelURCap
from model.joint_position_model import JointPositionModel
from model.move_j_command_model import MoveJCommandModel
from model.gripper_command_model import GripperCommandModel
from model.test.PayloadResponseModel import PayloadResponseModel

home_joint_position_model = JointPositionModel.get_joint_position_model_using_arguments(
    base=270, shoulder=-110, elbow=150, wrist1=-130, wrist2=270, wrist3=0)
retract_ct_01_joint_position_model = JointPositionModel.get_joint_position_model_using_arguments(
    base=270.80, shoulder=-89.49, elbow=150.18, wrist1=-58.70, wrist2=92.85, wrist3=180)
target_ct_01_joint_position_model = JointPositionModel.get_joint_position_model_using_arguments(
    base=272.88, shoulder=-75.48, elbow=131.96, wrist1=-54.50, wrist2=90.90, wrist3=179.95)

cg_joint_position_model = JointPositionModel.get_joint_position_model_using_arguments(
    base=129.8, shoulder=-98.45, elbow=164.32, wrist1=-66.57, wrist2=43.25, wrist3=180)
retract_bottom_position_model = JointPositionModel.get_joint_position_model_using_arguments(
    base=119.65, shoulder=-132.21, elbow=122.03, wrist1=10.9, wrist2=29.33, wrist3=179.34)
target_bottom_position_model = JointPositionModel.get_joint_position_model_using_arguments(
    base=150.09, shoulder=-107.03, elbow=110.14, wrist1=-2.62, wrist2=59.79, wrist3=179.77)

connection_string = ("HostName=AddQualIotHub.azure-devices.net;SharedAccessKeyName=service;"
                     "SharedAccessKey=X2vIeJ5i5kBJXNUaRLE0O7Btl0WZkaBFkAIoTGfyk7Y=")

# ur_cobot = "URCobot"
ur_gripper = "URGripper"


class LoadingHandler:
    def __init__(self, successor=None):
        self.successor = successor

    def handle(self):
        if self.successor:
            self.successor.handle()


# def move_j(joint_position_model_array):
#     move_j_command_model = MoveJCommandModel.get_move_j_command_model_using_arguments(
#         acceleration=0.3, velocity=0.3, time_s=0, blend_radius=0,
#         joint_position_model_array=joint_position_model_array)
#     method_payload = json.dumps(move_j_command_model, default=lambda o: o.__dict__, indent=1)
#     device_method = CloudToDeviceMethod(method_name="MoveJCommand", payload=method_payload)
#     registry_manager = IoTHubRegistryManager(connection_string)
#     response = registry_manager.invoke_device_method(ur_cobot, device_method)
#     json_response = json.loads(response.payload, object_hook=lambda d: PayloadResponseModel(**d))
#     print(json_response)
#     return json_response


def open_gripper():
    device_method = CloudToDeviceMethod(method_name="OpenGripperCommand")
    registry_manager = IoTHubRegistryManager(connection_string)
    response = registry_manager.invoke_device_method(ur_gripper, device_method)
    json_response = json.loads(response.payload, object_hook=lambda d: PayloadResponseModel(**d))
    print(json_response)
    return json_response


def close_gripper():
    device_method = CloudToDeviceMethod(method_name="CloseGripperCommand")
    registry_manager = IoTHubRegistryManager(connection_string)
    response = registry_manager.invoke_device_method(ur_gripper, device_method)
    json_response = json.loads(response.payload, object_hook=lambda d: PayloadResponseModel(**d))
    print(json_response)
    return json_response


def activate_gripper():
    device_method = CloudToDeviceMethod(method_name="ActivateGripperCommand")
    registry_manager = IoTHubRegistryManager(connection_string)
    response = registry_manager.invoke_device_method(ur_gripper, device_method)
    json_response = json.loads(response.payload, object_hook=lambda d: PayloadResponseModel(**d))
    print(json_response)
    return json_response


#

# class MoveHomeToRetractUnloadingPositionHandler(LoadingHandler):
#     def handle(self):
#         try:
#             joint_position_model_array = [home_joint_position_model, retract_ct_01_joint_position_model]
#             move_j(joint_position_model_array=joint_position_model_array)
#             super().handle()
#         except Exception:
#             raise Exception
#
#
# class MoveRetractUnloadingToTargetUnloadingPositionHandler(LoadingHandler):
#     def handle(self):
#         try:
#             joint_position_model_array = [retract_ct_01_joint_position_model, target_ct_01_joint_position_model]
#             move_j(joint_position_model_array=joint_position_model_array)
#             super().handle()
#         except Exception:
#             raise Exception
#
#
# class MoveTargetUnloadingToRetractUnloadingPositionHandler(LoadingHandler):
#     def handle(self):
#         try:
#             joint_position_model_array = [target_ct_01_joint_position_model, retract_ct_01_joint_position_model]
#             move_j(joint_position_model_array=joint_position_model_array)
#             super().handle()
#         except Exception:
#             raise Exception
#
#
# class MoveRetractUnloadingToCgPositionHandler(LoadingHandler):
#     def handle(self):
#         try:
#             joint_position_model_array = [retract_ct_01_joint_position_model, cg_joint_position_model]
#             move_j(joint_position_model_array=joint_position_model_array)
#             super().handle()
#         except Exception:
#             raise Exception
#
#
# class MoveCgToRetractLoadingPositionHandler(LoadingHandler):
#     def handle(self):
#         try:
#             joint_position_model_array = [cg_joint_position_model, retract_bottom_position_model]
#             move_j(joint_position_model_array=joint_position_model_array)
#             super().handle()
#         except Exception:
#             raise Exception
#
#
# class MoveRetractLoadingToTargetLoadingPositionHandler(LoadingHandler):
#     def handle(self):
#         try:
#             joint_position_model_array = [retract_bottom_position_model, target_bottom_position_model]
#             move_j(joint_position_model_array=joint_position_model_array)
#             super().handle()
#         except Exception:
#             raise Exception
#
#
# class MoveTargetLoadingToRetractLoadingPositionHandler(LoadingHandler):
#     def handle(self):
#         try:
#             joint_position_model_array = [target_bottom_position_model, retract_bottom_position_model]
#             move_j(joint_position_model_array=joint_position_model_array)
#             super().handle()
#         except Exception:
#             raise Exception
#
#
# class MoveRetractLoadingToCgPositionHandler(LoadingHandler):
#     def handle(self):
#         try:
#             joint_position_model_array = [retract_bottom_position_model, cg_joint_position_model]
#             move_j(joint_position_model_array=joint_position_model_array)
#             super().handle()
#         except Exception:
#             raise Exception
#
#
# class MoveCgToHomePositionHandler(LoadingHandler):
#     def handle(self):
#         try:
#             joint_position_model_array = [cg_joint_position_model, home_joint_position_model]
#             move_j(joint_position_model_array=joint_position_model_array)
#         except Exception:
#             raise Exception
#
#
# class ActivateGripperHandler(LoadingHandler):
#     def handle(self):
#         try:
#             ur_gripper = UrGripper("10.2.12.109")
#             ur_gripper.activate()
#             super().handle()
#         except Exception:
#             raise Exception
#
#
# class OpenGripperHandler(LoadingHandler):
#     def handle(self):
#         try:
#             ur_gripper = UrGripper("127.0.0.1")
#             ur_gripper.open_gripper()
#             super().handle()
#         except Exception:
#             raise Exception
#
#
# class CloseGripperHandler(LoadingHandler):
#     def handle(self):
#         try:
#             ur_gripper = UrGripper("127.0.0.1")
#             ur_gripper.close_gripper()
#             super().handle()
#         except Exception:
#             raise Exception


if __name__ == '__main__':
    close_gripper()
    # ur_gripper = URGripper("127.0.0.1")
    # ur_gripper.open_gripper()
    # ur_gripper.close_gripper()
    # close_gripper_payload_response_model = close_gripper()
    # print(close_gripper_payload_response_model)
    #
    # move_j_home_to_approach_position_payload_response_model = move_j_home_to_approach_position()
    # print(move_j_home_to_approach_position_payload_response_model)
    #
    # open_gripper_payload_response_model = open_gripper()
    # print(open_gripper_payload_response_model)

    # Client code

    # handlerA = ActivateGripperHandler()
    # handlerB = CloseGripperHandler()
    # handlerC = MoveHomeToRetractUnloadingPositionHandler()
    # handlerD = OpenGripperHandler()
    # handlerE = MoveRetractUnloadingToTargetUnloadingPositionHandler()
    # handlerF = CloseGripperHandler()
    # handlerG = MoveTargetUnloadingToRetractUnloadingPositionHandler()
    # handlerH = MoveRetractUnloadingToCgPositionHandler()

    # # handlerE = MoveCgToRetractLoadingPositionHandler()
    # # handlerF = MoveRetractLoadingToTargetLoadingPositionHandler()
    # # GripperHandlerC = OpenGripperHandler()
    # # handlerG = MoveTargetLoadingToRetractLoadingPositionHandler()
    # # GripperHandlerD = CloseGripperHandler()
    # # handlerH = MoveRetractLoadingToCgPositionHandler()
    # # handlerI = MoveCgToHomePositionHandler()
    #
    #
    # handlerA.successor = handlerB
    # handlerB.successor = handlerC
    # handlerC.successor = handlerD
    # handlerD.successor = handlerE
    # handlerE.successor = handlerF
    # handlerF.successor = handlerG
    # handlerG.successor = handlerH
    # handlerD.successor = handlerE
    # handlerE.successor = handlerF
    # handlerF.successor = GripperHandlerC
    # GripperHandlerC.successor = handlerG
    # handlerG.successor = GripperHandlerD
    # GripperHandlerD.successor = handlerH
    # handlerH.successor = handlerI

    # handlerA.handle()

    # try:
    #     # robot = urx.Robot("192.168.1.6")
    #     robot = urx.Robot("10.2.12.109")
    #     # robot = urx.Robot("localhost")
    #     print("Robot object is available as robot or r")
    # except Exception:
    #     print("exception")

    #     gripper.move_and_wait_for_pos(100, 255, 255)
    #     gripper.move_and_wait_for_pos(150, 255, 255)
    #     gripper.move_and_wait_for_pos(100, 255, 255)

    # robot = URGripper.Robot("10.2.12.109")
    # robotic_gripper = Robotiq_Two_Finger_Gripper(robot)
    # robotic_gripper.close_gripper()
    # robot.send_program(robotic_gripper._get_new_urscript)
    # robot.close()
