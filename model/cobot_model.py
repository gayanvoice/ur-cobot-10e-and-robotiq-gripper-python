from datetime import timedelta, datetime


class CobotModel(object):
    def __init__(self, name, moving_win=10):

        self.moving_window = moving_win
        self.records = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.index = 0

        self.cur = 0
        self.max = 0
        self.min = 0
        self.avg = 0

        self.name = name

    def record(self, current_temp):
        self.cur = current_temp
        self.records[self.index] = current_temp
        self.max = self.calculate_max(current_temp)
        self.min = self.calculate_min(current_temp)
        self.avg = self.calculate_average()

        self.index = (self.index + 1) % self.moving_window

    def calculate_max(self, current_temp):
        if not self.max:
            return current_temp
        elif current_temp > self.max:
            return self.max

    def calculate_min(self, current_temp):
        if not self.min:
            return current_temp
        elif current_temp < self.min:
            return self.min

    def calculate_average(self):
        return sum(self.records) / self.moving_window

    def create_report(self):
        response_dict = {}
        response_dict["maxTemp"] = self.max
        response_dict["minTemp"] = self.min
        response_dict["avgTemp"] = self.avg
        response_dict["startTime"] = (
            (datetime.now() - timedelta(0, self.moving_window * 8)).astimezone().isoformat()
        )
        response_dict["endTime"] = datetime.now().astimezone().isoformat()
        return response_dict
