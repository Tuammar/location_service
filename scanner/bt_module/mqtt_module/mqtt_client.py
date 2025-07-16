from ucollections import deque
from micropython import const, alloc_emergency_exception_buf
import ujson
from .umqtt_simple import MQTTClient

BUF_CAPACITY  = 10
MQTT_BROKER   = "31.56.196.111"
MQTT_PORT     = 1883
MQTT_USER     = 'scanner'
MQTT_PASS     = 'ble-scanner-very-strong-passwd'
CLIENT_ID     = "ble-scanner-16"
TOPIC         = b"ble/p-queue"
SCAN_INTERVAL = 30_000
GC_PERIOD_MS = 10000

def connect_mqtt():
    print("connecting to MQTT...")
    mqtt = MQTTClient(CLIENT_ID, MQTT_BROKER,
                      port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASS,
                      keepalive=60)
    mqtt.connect()
    print("MQTT connected")
    return mqtt

def send_message(mqtt_instance, message_dict):
    try:
        json_message = ujson.dumps(message_dict)
        mqtt_instance.publish(TOPIC, json_message)
        print(f"MQTT message sent: {json_message}")
    except Exception as e:
        print(f"Failed to send MQTT message: {e}")

def disconnect_mqtt(mqtt_instance):
    print("disconnecting from MQTT...")
    mqtt_instance.disconnect()

