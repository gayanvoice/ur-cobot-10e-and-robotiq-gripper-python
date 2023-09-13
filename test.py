import json
import time
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod

from model.joint_position_model import JointPositionModel
from model.move_j_command_model import MoveJCommandModel

home_joint_position_model = JointPositionModel.get_joint_position_model_using_arguments(
    base=270, shoulder=-110, elbow=150, wrist1=-130, wrist2=270, wrist3=0)
approach_ct_01_joint_position_model = JointPositionModel.get_joint_position_model_using_arguments(
    base=280.21, shoulder=-100.25, elbow=160.11, wrist1=-59.82, wrist2=99.58, wrist3=179.28)
joint_position_model_array = [home_joint_position_model, approach_ct_01_joint_position_model]

home_move_j_command_model = MoveJCommandModel.get_move_j_command_model_using_arguments(
    acceleration=0.5, velocity=0.5, time_s=0, blend_radius=0, joint_position_model_array=joint_position_model_array)

CONNECTION_STRING = ("HostName=AddQualIotHub.azure-devices.net;SharedAccessKeyName=service;"
                     "SharedAccessKey=X2vIeJ5i5kBJXNUaRLE0O7Btl0WZkaBFkAIoTGfyk7Y=")
DEVICE_ID = "CobotDevice"
METHOD_NAME = "MoveJCommand"
# METHOD_PAYLOAD = home_move_j_control_command_model.to_json()
METHOD_PAYLOAD = json.dumps(home_move_j_command_model, default=lambda o: o.__dict__, indent=1)
TIMEOUT = 60
WAIT_COUNT = 10


def iot_hub_device_method_sample_run():
    try:
        registry_manager = IoTHubRegistryManager(CONNECTION_STRING)
        device_method = CloudToDeviceMethod(method_name=METHOD_NAME, payload=METHOD_PAYLOAD)
        response = registry_manager.invoke_device_method(DEVICE_ID, device_method)

        print("")
        print("Successfully invoked the device to reboot.")

        print("")
        print(response.payload)

        while True:
            print("")
            print("IoTHubClient waiting for commands, press Ctrl-C to exit")

            status_counter = 0
            while status_counter <= WAIT_COUNT:
                twin_info = registry_manager.get_twin(DEVICE_ID)

                if twin_info.properties.reported.get("rebootTime") is not None:
                    print("Last reboot time: " + twin_info.properties.reported.get("rebootTime"))
                else:
                    print("Waiting for device to report last reboot time...")

                time.sleep(5)
                status_counter += 1

    except Exception as ex:
        print("")
        print("Unexpected error {0}".format(ex))
        return
    except KeyboardInterrupt:
        print("")
        print("IoTHubDeviceMethod sample stopped")


if __name__ == '__main__':
    iot_hub_device_method_sample_run()
