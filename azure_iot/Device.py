__author__ = "100638182"
__copyright__ = "AddQual"

import json

import numpy
from azure.iot.device import Message, MethodResponse
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device.aio import ProvisioningDeviceClient
import json
from json import JSONEncoder


class Device:

    def __init__(self, model_id, provisioning_host, id_scope, registration_id, symmetric_key):
        self.model_id = model_id
        self.provisioning_host = provisioning_host
        self.id_scope = id_scope
        self.registration_id = registration_id
        self.symmetric_key = symmetric_key
        self.iot_hub_device_client = None
        self.registration_result = None

    async def create_iot_hub_device_client(self):
        self.registration_result = await self.register_provisioning_device_client()

        if self.registration_result.status == "assigned":
            self.iot_hub_device_client = IoTHubDeviceClient.create_from_symmetric_key(
                symmetric_key=self.symmetric_key,
                hostname=self.registration_result.registration_state.assigned_hub,
                device_id=self.registration_result.registration_state.device_id,
                product_info=self.model_id)
            return self.iot_hub_device_client
        else:
            raise Exception("Device is not assigned")

    async def register_provisioning_device_client(self):
        provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
            provisioning_host=self.provisioning_host,
            registration_id=self.registration_id,
            id_scope=self.id_scope,
            symmetric_key=self.symmetric_key, )
        provisioning_device_client.provisioning_payload = {"modelId": self.model_id}
        return await provisioning_device_client.register()

    async def execute_command_listener(self, method_name, request_handler, response_handler):
        while True:
            if method_name:
                command_name = method_name
            else:
                command_name = None

            command_request = await self.iot_hub_device_client.receive_method_request(command_name)
            request_payload = {}
            if command_request.payload:
                request_payload = command_request.payload

            response_model = await request_handler(request_payload)

            response_status = 200
            response_payload = response_handler(response_model)

            command_response = MethodResponse.create_from_method_request(command_request, response_status,
                                                                         response_payload)

            try:
                await self.iot_hub_device_client.send_method_response(command_response)
            except Exception as ex:
                print(ex)

    async def send_telemetry(self, telemetry):
        telemetry_json = json.dumps(telemetry, cls=NumpyArrayEncoder)
        message = Message(telemetry_json)
        message.content_encoding = "utf-8"
        message.content_type = "application/json"
        await self.iot_hub_device_client.send_message(message)


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)
