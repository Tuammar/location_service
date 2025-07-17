import paho.mqtt.client as mqtt
import json
import redis
import os
from datetime import datetime

# Redis connection
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', '6379')),
    db=0,
    decode_responses=True
)

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
        timestamp = datetime.now().isoformat()
        
        # Add timestamp to payload
        payload['received_at'] = timestamp
        payload['topic'] = message.topic
        
        print(f"Received message from {message.topic}: {payload}")
        userdata.append(payload)
        
        # Save to Redis
        redis_key = f"data:{message.topic}"
        redis_client.lpush(redis_key, json.dumps(payload))
        
        # Keep only last 1000 messages per topic
        redis_client.ltrim(redis_key, 0, 999)
        
        # Also save latest data by topic
        redis_client.hset("latest_data", message.topic, json.dumps(payload))
        
        print(f"Saved to Redis: {redis_key}")
        
    except json.JSONDecodeError:
        print(f"Failed to decode JSON: {message.payload}")
    except Exception as e:
        print(f"Error saving to Redis: {e}")
    
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


# MQTT Configuration from environment variables
broker = os.getenv('MQTT_BROKER')
port = int(os.getenv('MQTT_PORT'))
topic = os.getenv('MQTT_TOPIC')
client_id = f'subscriber-backend'
username = os.getenv('MQTT_USERNAME')
password = os.getenv('MQTT_PASSWORD')

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)

mqttc.username_pw_set(username, password)

mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

mqttc.user_data_set([])

print(f"Connecting to {broker}:{port} as {username}...")
print(f"Redis connection: {redis_client.ping()}")

mqttc.connect(broker, port, 60)
mqttc.loop_forever()
print(f"Received the following messages: {mqttc.user_data_get()}")