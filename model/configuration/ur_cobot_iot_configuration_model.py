import xml.etree.ElementTree as ET


class URCobotIotConfigurationModel:
    def __init__(self):
        self._model_id = None
        self._provisioning_host = None
        self._id_scope = None
        self._registration_id = None
        self._symmetric_key = None
        self._host = None
        self._dashboard_server_port = None
        self._primary_port = None
        self._secondary_port = None
        self._real_time_port = None
        self._rtde_port = None

    @property
    def model_id(self):
        return self._model_id

    @property
    def provisioning_host(self):
        return self._provisioning_host

    @property
    def id_scope(self):
        return self._id_scope

    @property
    def registration_id(self):
        return self._registration_id

    @property
    def symmetric_key(self):
        return self._symmetric_key

    @property
    def host(self):
        return self._host

    @property
    def dashboard_server_port(self):
        return self._dashboard_server_port

    @property
    def primary_port(self):
        return self._primary_port

    @property
    def secondary_port(self):
        return self._secondary_port

    @property
    def real_time_port(self):
        return self._real_time_port

    @property
    def rtde_port(self):
        return self._rtde_port

    @model_id.setter
    def model_id(self, value):
        self._model_id = value

    @provisioning_host.setter
    def provisioning_host(self, value):
        self._provisioning_host = value

    @id_scope.setter
    def id_scope(self, value):
        self._id_scope = value

    @registration_id.setter
    def registration_id(self, value):
        self._registration_id = value

    @symmetric_key.setter
    def symmetric_key(self, value):
        self._symmetric_key = value

    @host.setter
    def host(self, value):
        self._host = value

    @dashboard_server_port.setter
    def dashboard_server_port(self, value):
        self._dashboard_server_port = int(value)

    @primary_port.setter
    def primary_port(self, value):
        self._primary_port = int(value)

    @secondary_port.setter
    def secondary_port(self, value):
        self._secondary_port = int(value)

    @real_time_port.setter
    def real_time_port(self, value):
        self._real_time_port = int(value)

    @rtde_port.setter
    def rtde_port(self, value):
        self._rtde_port = int(value)

    def get(self, iot_configuration_xml_file_path):
        iot_configuration_element_tree = ET.parse(iot_configuration_xml_file_path)
        self.model_id = iot_configuration_element_tree.find('./ur_cobot/model_id').text
        self.provisioning_host = iot_configuration_element_tree.find('./ur_cobot/provisioning_host').text
        self.id_scope = iot_configuration_element_tree.find('./ur_cobot/id_scope').text
        self.registration_id = iot_configuration_element_tree.find('./ur_cobot/registration_id').text
        self.symmetric_key = iot_configuration_element_tree.find('./ur_cobot/symmetric_key').text
        self.host = iot_configuration_element_tree.find('./ur_cobot/host').text
        self.dashboard_server_port = iot_configuration_element_tree.find('./ur_cobot/dashboard_server_port').text
        self.primary_port = iot_configuration_element_tree.find('./ur_cobot/primary_port').text
        self.secondary_port = iot_configuration_element_tree.find('./ur_cobot/secondary_port').text
        self.real_time_port = iot_configuration_element_tree.find('./ur_cobot/real_time_port').text
        self.rtde_port = iot_configuration_element_tree.find('./ur_cobot/rtde_port').text
        return self
