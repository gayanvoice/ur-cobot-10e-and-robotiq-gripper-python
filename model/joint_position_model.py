__author__ = "Gayan Kuruppu"
__copyright__ = "AddQual"

import json
import math


class JointPositionModel:
    def __init__(self):
        self._base = None
        self._shoulder = None
        self._elbow = None
        self._wrist1 = None
        self._wrist2 = None
        self._wrist3 = None

    @property
    def base(self):
        return self._base

    @property
    def shoulder(self):
        return self._shoulder

    @property
    def elbow(self):
        return self._elbow

    @property
    def wrist1(self):
        return self._wrist1

    @property
    def wrist2(self):
        return self._wrist2

    @property
    def wrist3(self):
        return self._wrist3

    @base.setter
    def base(self, value):
        self._base = value

    @shoulder.setter
    def shoulder(self, value):
        self._shoulder = value

    @elbow.setter
    def elbow(self, value):
        self._elbow = value

    @wrist1.setter
    def wrist1(self, value):
        self._wrist1 = value

    @wrist2.setter
    def wrist2(self, value):
        self._wrist2 = value

    @wrist3.setter
    def wrist3(self, value):
        self._wrist3 = value

    @staticmethod
    def get_joint_position_model_from_joint_position_model_object(joint_position_model_object):
        joint_position_model = JointPositionModel()
        joint_position_model.base = joint_position_model_object["_base"]
        joint_position_model.shoulder = joint_position_model_object["_shoulder"]
        joint_position_model.elbow = joint_position_model_object["_elbow"]
        joint_position_model.wrist1 = joint_position_model_object["_wrist1"]
        joint_position_model.wrist2 = joint_position_model_object["_wrist2"]
        joint_position_model.wrist3 = joint_position_model_object["_wrist3"]
        return joint_position_model

    @staticmethod
    def get_position_array_from_joint_position_model(joint_position_model):
        return (math.radians(joint_position_model.base),
                math.radians(joint_position_model.shoulder),
                math.radians(joint_position_model.elbow),
                math.radians(joint_position_model.wrist1),
                math.radians(joint_position_model.wrist2),
                math.radians(joint_position_model.wrist3))

    @staticmethod
    def get_joint_position_model_using_arguments(base, shoulder, elbow, wrist1, wrist2, wrist3):
        joint_position_model = JointPositionModel()
        joint_position_model.base = base
        joint_position_model.shoulder = shoulder
        joint_position_model.elbow = elbow
        joint_position_model.wrist1 = wrist1
        joint_position_model.wrist2 = wrist2
        joint_position_model.wrist3 = wrist3
        return joint_position_model
