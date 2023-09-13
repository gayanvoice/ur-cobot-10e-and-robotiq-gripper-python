import asyncio

import URBasic
from azure_iot.CobotDevice import CobotDevice
from model.joint_position_model import JointPositionModel

host = '10.2.12.109'


# def move_command(ur_script_ext):
#     # joint position models
#     home_joint_position_model = JointPositionModel.get_joint_position_model(
#         base=270, shoulder=-110, elbow=150, wrist1=-130, wrist2=270, wrist3=0)
#     approach_ct_01_joint_position_model = JointPositionModel.get_joint_position_model(
#         base=280.21, shoulder=-100.25, elbow=160.11, wrist1=-59.82, wrist2=99.58, wrist3=179.28)
#
#     target_ct_01_joint_position_model = JointPositionModel.get_joint_position_model(
#         base=273.56, shoulder=-74.36, elbow=131.73, wrist1=-57.33, wrist2=92.9, wrist3=179.3)
#
#     cg_joint_position_model = JointPositionModel.get_joint_position_model(
#         base=129.8, shoulder=-98.45, elbow=164.32, wrist1=-66.57, wrist2=43.25, wrist3=180)
#
#     approach_bottom_joint_position_model = JointPositionModel.get_joint_position_model(
#         base=119.65, shoulder=-132.21, elbow=122.03, wrist1=-10.9, wrist2=29.33, wrist3=179.34)
#
#     target_bottom_joint_position_model = JointPositionModel.get_joint_position_model(
#         base=150.09, shoulder=-107.03, elbow=110.14, wrist1=-2.62, wrist2=59.79, wrist3=179.77)
#
#     # move j control command models
#     home_move_j_control_command_model = MoveJControlCommandModel.get_move_j_control_command_model(
#         acceleration=0.5, velocity=0.5, time_s=0, blend_radius=0,
#         joint_position_model_array=home_joint_position_model)
#
#     approach_ct_01_move_j_control_command_model = MoveJControlCommandModel.get_move_j_control_command_model(
#         acceleration=0.5, velocity=0.5, time_s=0, blend_radius=0,
#         joint_position_model_array=approach_ct_01_joint_position_model)
#
#     target_ct_o1_move_j_control_command_model = MoveJControlCommandModel.get_move_j_control_command_model(
#         acceleration=0.5, velocity=0.5, time_s=0, blend_radius=0,
#         joint_position_model_array=target_ct_01_joint_position_model)
#
#     cg_move_j_control_command_model = MoveJControlCommandModel.get_move_j_control_command_model(
#         acceleration=0.5, velocity=0.5, time_s=0, blend_radius=0,
#         joint_position_model_array=cg_joint_position_model)
#
#     approach_bottom_move_j_control_command_model = MoveJControlCommandModel.get_move_j_control_command_model(
#         acceleration=0.5, velocity=0.5, time_s=0, blend_radius=0,
#         joint_position_model_array=approach_bottom_joint_position_model)
#
#     target_bottom_move_j_control_command_model = MoveJControlCommandModel.get_move_j_control_command_model(
#         acceleration=0.5, velocity=0.5, time_s=0, blend_radius=0,
#         joint_position_model_array=target_bottom_joint_position_model)
#
#     execute_move_j_command(ur_script_ext=ur_script_ext, move_j_control_model=home_move_j_control_command_model)
#     execute_move_j_command(ur_script_ext=ur_script_ext,
#                            move_j_control_model=approach_ct_01_move_j_control_command_model)
#     execute_move_j_command(ur_script_ext=ur_script_ext, move_j_control_model=target_ct_o1_move_j_control_command_model)
#     # execute_gripper_program_command()
#     execute_move_j_command(ur_script_ext=ur_script_ext, move_j_control_model=target_ct_o1_move_j_control_command_model)
#     execute_move_j_command(ur_script_ext=ur_script_ext,
#                            move_j_control_model=approach_ct_01_move_j_control_command_model)
#     execute_move_j_command(ur_script_ext=ur_script_ext, move_j_control_model=cg_move_j_control_command_model)
#     execute_move_j_command(ur_script_ext=ur_script_ext,
#                            move_j_control_model=approach_bottom_move_j_control_command_model)
#     execute_move_j_command(ur_script_ext=ur_script_ext, move_j_control_model=target_bottom_move_j_control_command_model)
#     # # execute_gripper_program_command()
#     # execute_move_j_command(move_j_control_model=target_bottom_move_j_control_command_model)
#     # execute_move_j_command(move_j_control_model=approach_bottom_move_j_control_command_model)
#     # execute_move_j_command(move_j_control_model=cg_move_j_control_command_model)
#     # execute_move_j_command(move_j_control_model=approach_ct_01_move_j_control_command_model)
#     # execute_move_j_command(move_j_control_model=target_ct_o1_move_j_control_command_model)
#     # # execute gripper program_command()
#     # execute_move_j_command(move_j_control_model=target_ct_o1_move_j_control_command_model)
#     # execute_move_j_command(move_j_control_model=approach_ct_01_move_j_control_command_model)
#     # execute_move_j_command(move_j_control_model=home_move_j_control_command_model)
#

# def execute_move_j_command(ur_script_ext, move_j_control_model):
#     ur_script_ext.movej(q=move_j_control_model.joint_position_model_array,
#                         a=move_j_control_model.acceleration,
#                         v=move_j_control_model.velocity,
#                         t=move_j_control_model.time_s,
#                         r=move_j_control_model.blend_radius)
#
#
# def execute_gripper_program_command(ur_script_ext):
#     ur_script_ext.load_program('gripper.urp')
#     ur_script_ext.play_program()

async def main():
    try:
        queue = asyncio.Queue()
        cobot_device = CobotDevice()
        await asyncio.gather(cobot_device.connect_azure_iot(queue))
    except asyncio.exceptions.CancelledError:
        print("main:The execution of the thread was manually stopped due to a KeyboardInterrupt signal.")
    except SystemExit:
        print("main:Cobot client was stopped.")

if __name__ == '__main__':
    asyncio.run(main())

