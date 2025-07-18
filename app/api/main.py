from fastapi import FastAPI
import redis
import json
import os
from core.distance_calculator import distance_calculator

app = FastAPI()

redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', '6379')),
    db=0,
    decode_responses=True
)

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/api/latest")
def get_latest():
    latest_data = redis_client.hgetall("latest_data")
    return {k: json.loads(v) for k, v in latest_data.items()}

@app.get("/api/history")
def get_history():
    history_data = {}
    for topic in redis_client.hkeys("latest_data"):
        data_list = redis_client.lrange(f"data:{topic}", 0, 99)
        history_data[topic] = [json.loads(item) for item in data_list]
    return history_data

@app.get("/api/history/cu_C_beacon")
def history_cu_C_beacon():
    data_list = redis_client.lrange("rssi:cu_C_beacon", 0, 99)
    return [json.loads(item) for item in data_list]

@app.get("/api/history/cu_A_beacon")
def history_cu_A_beacon():
    data_list = redis_client.lrange("rssi:cu_A_beacon", 0, 99)
    return [json.loads(item) for item in data_list]

@app.get("/api/history/cu_B_beacon")
def history_cu_B_beacon():
    data_list = redis_client.lrange("rssi:cu_B_beacon", 0, 99)
    return [json.loads(item) for item in data_list]

@app.get("/api/history/cu_D_beacon")
def history_cu_D_beacon():
    data_list = redis_client.lrange("rssi:cu_D_beacon", 0, 99)
    return [json.loads(item) for item in data_list]

@app.get("/api/distances")
def get_distances():
    beacons = ["cu_C_beacon", "cu_A_beacon", "cu_B_beacon", "cu_D_beacon"]
    result = {}
    for beacon in beacons:
        data = redis_client.lindex(f"rssi:{beacon}", 0)
        if data:
            payload = json.loads(data)
            rssi = payload.get("rssi")
            tx_power = payload.get("tx_power", -69)
            if rssi is not None:
                distance = distance_calculator(rssi, tx_power=tx_power)
                result[beacon] = distance
            else:
                result[beacon] = None
        else:
            result[beacon] = None
    return result
