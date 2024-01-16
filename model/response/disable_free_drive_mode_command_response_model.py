from model.response.response_model import ResponseModel


class DisableFreeDriveModeCommandResponseModel(ResponseModel):
    def __init__(self):
        super().__init__()
        self._status = None
        self._message = None

    def get_disable_free_drive_mode_command_response_model(self, status):
        response_model = super().get(status=status)
        self._status = response_model.status
        return self

    def get_successfully_executed(self):
        self.get_disable_free_drive_mode_command_response_model(status=True)
        self._message = "disable free drive mode command executed successfully"
        return self

    def get_exception(self, exception):
        self.get_disable_free_drive_mode_command_response_model(status=False)
        self._message = exception
        return self

