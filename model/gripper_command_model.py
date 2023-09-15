import json


class GripperCommandModel:
    def __init__(self):
        self._method = None

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, value):
        self._method = value

    @staticmethod
    def get_gripper_command_model_using_request_payload(request_payload):
        json_request_payload = json.loads(request_payload)
        gripper_command_model = GripperCommandModel()
        gripper_command_model.acceleration = json_request_payload["_method"]
        return gripper_command_model

    @staticmethod
    def get_gripper_command_model_using_arguments(method):
        gripper_command_model = GripperCommandModel()
        gripper_command_model.acceleration = method
        return gripper_command_model
