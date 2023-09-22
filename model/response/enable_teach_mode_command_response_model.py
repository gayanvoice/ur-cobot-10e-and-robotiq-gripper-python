from model.response.response_model import ResponseModel


class EnableTeachModeCommandResponseModel(ResponseModel):
    def __init__(self):
        super().__init__()
        self._status = None
        self._message = None

    def get_enable_teach_mode_command_response_model(self, status):
        response_model = super().get(status=status)
        self._status = response_model.statuss
        return self

    def get_successfully_executed(self):
        self.get_enable_teach_mode_command_response_model(status=True)
        self._message = "enable teach mode command executed successfully"
        return self

    def get_exception(self, exception):
        self.get_enable_teach_mode_command_response_model(status=False)
        self._message = exception
        return self

