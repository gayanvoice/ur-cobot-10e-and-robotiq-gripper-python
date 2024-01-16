import json
from model.joint_position_model import JointPositionModel


class MoveJCommandModel:
    def __init__(self):
        self._acceleration = None
        self._velocity = None
        self._time_s = None
        self._blend_radius = None
        self._joint_position_model_array = []

    @property
    def acceleration(self):
        return self._acceleration

    @property
    def velocity(self):
        return self._velocity

    @property
    def time_s(self):
        return self._time_s

    @property
    def blend_radius(self):
        return self._blend_radius

    @property
    def joint_position_model_array(self):
        return self._joint_position_model_array

    @acceleration.setter
    def acceleration(self, value):
        self._acceleration = value

    @velocity.setter
    def velocity(self, value):
        self._velocity = value

    @time_s.setter
    def time_s(self, value):
        self._time_s = value

    @blend_radius.setter
    def blend_radius(self, value):
        self._blend_radius = value

    @joint_position_model_array.setter
    def joint_position_model_array(self, value):
        self._joint_position_model_array.append(value)

    def validate(self):
        if self._acceleration > 0.5:
            raise Exception("invalid acceleration value:" + str(self._acceleration) + " value must be less than 0.5")
        if self._velocity > 0.5:
            raise Exception("invalid velocity value:" + str(self._velocity) + " value must be less than 0.5")
        for joint_position_model in self._joint_position_model_array:
            if 0 > joint_position_model.base <= 270:
                raise Exception("invalid base value:" + str(joint_position_model.base) + " value range 0 - 270")
            if 0 > joint_position_model.shoulder <= 270:
                raise Exception("invalid shoulder value:" + str(joint_position_model.shoulder) + " value range 0 - 270")
            if 0 > joint_position_model.elbow <= 270:
                raise Exception("invalid elbow value:" + str(joint_position_model.elbow) + " value range 0 - 270")
            if 0 > joint_position_model.wrist1 <= 270:
                raise Exception("invalid wrist1 value:" + str(joint_position_model.wrist1) + " value range 0 - 270")
            if 0 > joint_position_model.wrist2 <= 270:
                raise Exception("invalid wrist2 value:" + str(joint_position_model.wrist2) + " value range 0 - 270")
            if 0 > joint_position_model.wrist3 <= 270:
                raise Exception("invalid wrist3 value:" + str(joint_position_model.wrist3) + " value range 0 - 270")

    @staticmethod
    def get_move_j_command_model_using_request_payload(request_payload):
        json_str = json.dumps(request_payload)
        json_request_payload = json.loads(json_str)
        move_j_command_model = MoveJCommandModel()
        move_j_command_model.acceleration = json_request_payload["_acceleration"]
        move_j_command_model.velocity = json_request_payload["_velocity"]
        move_j_command_model.time_s = json_request_payload["_time_s"]
        move_j_command_model.blend_radius = json_request_payload["_blend_radius"]
        for joint_position_model_object in json_request_payload["_joint_position_model_array"]:
            joint_position_model = JointPositionModel\
                .get_joint_position_model_from_joint_position_model_object(joint_position_model_object)
            move_j_command_model.joint_position_model_array = joint_position_model
        return move_j_command_model

    @staticmethod
    def get_move_j_command_model_using_arguments(
            acceleration, velocity, time_s, blend_radius, joint_position_model_array):
        move_j_command_model = MoveJCommandModel()
        move_j_command_model.acceleration = acceleration
        move_j_command_model.velocity = velocity
        move_j_command_model.time_s = time_s
        move_j_command_model.blend_radius = blend_radius
        for joint_position_model in joint_position_model_array:
            move_j_command_model.joint_position_model_array = joint_position_model
        return move_j_command_model
