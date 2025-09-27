from arctis_manager.device_manager import (DeviceState, DeviceManager,
                                           DeviceStatus, InterfaceEndpoint)

VOLUME_MESSAGE = 0x45

class Arctis7Wireless(DeviceManager):
    def init_device(self):
        self.game = 1.0
        self.chat = 1.0

    def get_device_product_id(self) -> int:
        return 0x2202

    def get_device_name(self) -> str:
        return 'Arctis Nova 7 Wireless'

    def manage_input_data(self, data: list[int], endpoint: InterfaceEndpoint) -> DeviceState:
        if endpoint == self.utility_guess_endpoint(7, 'in'):
            # The first byte appears to indicate a message type
            # 0x45 contains volume information
            # I've also seen 0xbb, 0xb7 and 0xb9 messages but I'm not sure what the format is
            if data[0] == VOLUME_MESSAGE:
                self.game = data[1] / 100
                self.chat = data[2] / 100
            return DeviceState(self.game, self.chat, 1, 1, DeviceStatus())

    def get_endpoint_addresses_to_listen(self) -> list[InterfaceEndpoint]:
        return [self.utility_guess_endpoint(7, 'in')]

    def get_request_device_status(self):
        return self.utility_guess_endpoint(7, 'out'), [0x06, 0xb0]
