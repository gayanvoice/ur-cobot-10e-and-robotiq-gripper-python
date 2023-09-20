import xml.etree.ElementTree as ET


class SharedIotConfigurationModel:
    def __init__(self):
        self._telemetry_delay = None

    @property
    def telemetry_delay(self):
        return self._telemetry_delay

    @telemetry_delay.setter
    def telemetry_delay(self, value):
        self._telemetry_delay = float(value)

    def get(self, iot_configuration_xml_file_path):
        iot_configuration_element_tree = ET.parse(iot_configuration_xml_file_path)
        self.telemetry_delay = iot_configuration_element_tree.find('./shared/telemetry_delay').text
        return self
