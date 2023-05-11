import os

from ..settings import settings
from ..models import LampData


class LampControl:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(LampControl, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.cache_lamp_values = {
            os.path.join(settings.mqtt_topic_lamp, id_): LampData(
                lamp_number=num
            )
            for num, id_ in enumerate(settings.mqtt_lamp_idl, 1)
        }
        self.lamp_number_id_map = {
            num: os.path.join(settings.mqtt_topic_lamp, id_)
            for num, id_ in enumerate(settings.mqtt_lamp_idl, 1)
        }

    async def get_lamp_data(self, lamp_number: int) -> LampData:
        return self.cache_lamp_values[self.lamp_number_id_map[lamp_number]]

    async def set_lamp_temperature(self, lamp_number: int):
        pass

    async def set_lamp_brightness(self, lamp_number: int):
        pass
