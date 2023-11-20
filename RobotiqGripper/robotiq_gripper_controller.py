import re
import socket
from time import sleep


class RobotiqGripperController:
    # WRITE VARIABLES
    ACT = 'ACT'  # act : activate (1 while activated, can be reset to clear fault status)
    GTO = 'GTO'  # gto : go to (will perform go to with the actions set in pos, for, spe)
    ATR = 'ATR'  # atr : auto-release (emergency slow move)
    ADR = 'ADR'  # adr : auto-release direction (open(1) or close(0) during auto-release)
    FOR = 'FOR'  # for : force (0-255)
    SPE = 'SPE'  # spe : speed (0-255)
    POS = 'POS'  # pos : position (0-255), 0 = open
    # READ VARIABLES
    STA = 'STA'  # status (0 = is reset, 1 = activating, 3 = active)
    PRE = 'PRE'  # position request (echo of last commanded position)
    OBJ = 'OBJ'  # object detection (0 = moving, 1 = outer grip, 2 = inner grip, 3 = no object at rest)
    FLT = 'FLT'  # fault (0=ok, see manual for errors if not zero)

    ENCODING = 'UTF-8'  # ASCII and UTF-8 both seem to work

    ACT_GRIPPER_RESET = 0
    ACT_GRIPPER_ACTIVATE = 1

    GTO_GRIPPER_STOP = 0
    GTO_GRIPPER_START = 1

    OBJ_GRIPPER_MOVE_TO_POSITION = 0
    OBJ_GRIPPER_STOP_BEFORE_OPEN_POSITION = 1
    OBJ_GRIPPER_STOP_BEFORE_CLOSE_POSITION = 2
    OBJ_GRIPPER_IN_POSITION = 3

    def __init__(self):
        self.socket = None

    def connect(self, hostname, port=63352, socket_timeout=2.0):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((hostname, port))
        self.socket.settimeout(socket_timeout)

    def disconnect(self):
        self.socket.close()

    def get_position(self):
        pattern = r'POS (\d+)'
        command = self.get_command(self.POS)
        output = self.send_command(command=command)
        match = re.search(pattern, output.decode())
        if match:
            return int(match.group(1))
        else:
            return -1

    def get_activate(self):
        pattern = r'ACT (\d+)'
        command = self.get_command(self.ACT)
        output = self.send_command(command=command)
        match = re.search(pattern, output.decode())
        if match:
            return int(match.group(1))
        else:
            return -1

    def get_goto(self):
        pattern = r'GTO (\d+)'
        command = self.get_command(self.GTO)
        output = self.send_command(command=command)
        match = re.search(pattern, output.decode())
        if match:
            return int(match.group(1))
        else:
            return -1

    def get_force(self):
        pattern = r'FOR (\d+)'
        command = self.get_command(self.FOR)
        output = self.send_command(command=command)
        match = re.search(pattern, output.decode())
        if match:
            return int(match.group(1))
        else:
            return -1

    def get_speed(self):
        pattern = r'SPE (\d+)'
        command = self.get_command(self.SPE)
        output = self.send_command(command=command)
        match = re.search(pattern, output.decode())
        if match:
            return int(match.group(1))
        else:
            return -1

    def get_status(self):
        pattern = r'STA (\d+)'
        command = self.get_command(self.STA)
        output = self.send_command(command=command)
        match = re.search(pattern, output.decode())
        if match:
            return int(match.group(1))
        else:
            return -1

    def get_position_request(self):
        pattern = r'PRE (\d+)'
        command = self.get_command(self.PRE)
        output = self.send_command(command=command)
        match = re.search(pattern, output.decode())
        if match:
            return int(match.group(1))
        else:
            return -1

    def get_object_detection(self):
        pattern = r'OBJ (\d+)'
        command = self.get_command(self.OBJ)
        output = self.send_command(command=command)
        match = re.search(pattern, output.decode())
        if match:
            return int(match.group(1))
        else:
            return -1

    def get_fault(self):
        pattern = r'FLT (\d+)'
        command = self.get_command(self.FLT)
        output = self.send_command(command=command)
        match = re.search(pattern, output.decode())
        if match:
            return int(match.group(1))
        else:
            return -1

    def send_command(self, command):
        self.socket.sendall(command)
        return self.socket.recv(2 ** 10)

    def move_gripper(self, position, speed=10, force=10):
        set_gripper_stop = self.set_command(self.GTO, self.GTO_GRIPPER_STOP)
        set_speed = self.set_command(self.SPE, speed)
        set_force = self.set_command(self.FOR, force)
        set_position = self.set_command(self.POS, position)
        set_gripper_start = self.set_command(self.GTO, self.GTO_GRIPPER_START)
        command_array = [set_gripper_stop, set_speed, set_force, set_position, set_gripper_start]
        for command in command_array:
            self.send_command(command)
        while True:
            sleep(0.5)
            if self.get_object_detection() == self.OBJ_GRIPPER_IN_POSITION:
                return True
            if (self.get_object_detection() == self.OBJ_GRIPPER_STOP_BEFORE_OPEN_POSITION) or (
                    self.get_object_detection() == self.OBJ_GRIPPER_STOP_BEFORE_CLOSE_POSITION):
                return False

    def activate(self):
        if self.get_activate() == self.ACT_GRIPPER_RESET:
            set_act = self.set_command(self.ACT, self.ACT_GRIPPER_ACTIVATE)
            self.send_command(set_act)
            while True:
                sleep(0.5)
                if self.get_activate() == self.ACT_GRIPPER_ACTIVATE:
                    return True
                else:
                    return False

    def open_gripper(self):
        return self.move_gripper(0)

    def close_gripper(self):
        return self.move_gripper(255)

    @staticmethod
    def get_command(action):
        return b'GET ' + str(action).encode() + b'\n'

    @staticmethod
    def set_command(action, value):
        return b'SET ' + str(action).encode() + b' ' + str(value).encode() + b'\n'