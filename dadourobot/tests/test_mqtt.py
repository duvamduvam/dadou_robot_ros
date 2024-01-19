import time
import unittest

from dadou_utils.com.mqtt_client import MQTT_client

class MQTTTest(unittest.TestCase):


    def test_connect(self):
        print("connect")

        mqtt_client = MQTT_client()

        print("messages")

        msg_count = 1
        topic = "Didier"
        while True:
            time.sleep(1)
            mqtt_client.publish("msg {}".format(msg_count))
            msg_count += 1

            if msg_count > 5:
                break




