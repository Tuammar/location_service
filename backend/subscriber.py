import paho.mqtt.client as mqtt
import json

def on_subscribe(client, userdata, mid, reason_code_list, properties):
    if reason_code_list[0].is_failure:
        print(f"Broker rejected you subscription: {reason_code_list[0]}")
    else:
        print(f"Broker granted the following QoS: {reason_code_list[0].value}")

def on_unsubscribe(client, userdata, mid, reason_code_list, properties):
    if len(reason_code_list) == 0 or not reason_code_list[0].is_failure:
        print("unsubscribe succeeded (if SUBACK is received in MQTTv3 it success)")
    else:
        print(f"Broker replied with failure: {reason_code_list[0]}")
    client.disconnect()

def on_message(client, userdata, message):
    try:
        payload = json.loads(message.payload.decode())
        print(f"Received message from {message.topic}: {payload}")
        userdata.append(payload)
        
        # TODO: Здесь добавить сохранение в Redis
        # redis_client.lpush(f"data:{message.topic}", json.dumps(payload))
        
    except json.JSONDecodeError:
        print(f"Failed to decode JSON: {message.payload}")
    
    # We only want to process 10 messages for demo
    if len(userdata) >= 10:
        client.unsubscribe(topic)

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
    else:
        print(f"Connected to broker {broker}:{port}")
        client.subscribe(topic)
        print(f"Subscribed to topic: {topic}")



broker = "31.56.196.111"
port = 1883
topic = "ble/p-queue"
client_id = f'subscriber-backend'
username = 'scanner'
password = 'ble-scanner-very-strong-passwd'

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)

mqttc.username_pw_set(username, password)

mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

mqttc.user_data_set([])

print(f"Connecting to {broker}:{port} as {username}...")
mqttc.connect(broker, port, 60)
mqttc.loop_forever()
print(f"Received the following messages: {mqttc.user_data_get()}")