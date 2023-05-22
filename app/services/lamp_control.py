import re

from fastapi_mqtt import FastMQTT, MQTTConfig

from ..settings import settings
from ..models import LampData


class LampControl:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(LampControl, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.mqtt = FastMQTT(
            MQTTConfig(host=settings.mqtt_host, port=settings.mqtt_port)
        )
        self.topic_lamp_re_pattern = settings.mqtt_topic_lamp_pattern.format(
            id="(\S+)", measure="(\S.+)"
        )
        self.lamp_number_id_map = {
            num: id_ for num, id_ in enumerate(settings.mqtt_lamp_ids, 1)
        }
        self.cache_lamp_values = {
            self.lamp_number_id_map[num]: LampData(lamp_number=num)
            for num in self.lamp_number_id_map
        }
        self._handlers_create()

    def _handlers_create(self):
        topics = []
        for lamp_id in settings.mqtt_lamp_ids:
            for measure in (
                settings.mqtt_lamp_bright_measure,
                settings.mqtt_lamp_temp_measure,
            ):
                topics.append(
                    settings.mqtt_topic_lamp_pattern.format(
                        id=lamp_id, measure=measure
                    )
                )

        @self.mqtt.subscribe(*topics)
        async def message_from_topic(client, topic, payload, qos, properties):
            lamp_id = re.search(self.topic_lamp_re_pattern, topic).group(1)
            if settings.mqtt_lamp_bright_measure in topic:
                self.cache_lamp_values[lamp_id].brightness = int(
                    int(payload.decode())
                )
            elif settings.mqtt_lamp_temp_measure in topic:
                self.cache_lamp_values[lamp_id].temperature = int(
                    int(payload.decode())
                )

    def get_lamp_data(self, lamp_number: int) -> LampData:
        lamp_id = self.lamp_number_id_map[lamp_number]
        return self.cache_lamp_values[lamp_id]

    def set_lamp_data(self, lamp_data: LampData):
        lamp_id = self.lamp_number_id_map[lamp_data.lamp_number]
        self.mqtt.publish(
            settings.mqtt_topic_lamp_pattern.format(
                id=lamp_id, measure=settings.mqtt_lamp_temp_measure
            ),
            lamp_data.temperature,
        )
        self.mqtt.publish(
            settings.mqtt_topic_lamp_pattern.format(
                id=lamp_id, measure=settings.mqtt_lamp_bright_measure
            ),
            lamp_data.brightness,
        )
