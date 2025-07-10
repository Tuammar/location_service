from micropython import const
import ubluetooth, utime

AD_TYPE_FLAGS = const(0x01)
AD_TYPE_COMPLETE_LOCAL_NAME = const(0x09)

FLAGS_GENERAL_DISCOVERY = const(0x06) 

device_name = "cu_2025_beacon"

def create_advertising_data(name):
    flags_data = bytes([AD_TYPE_FLAGS, FLAGS_GENERAL_DISCOVERY])
    
    name_data = bytes([AD_TYPE_COMPLETE_LOCAL_NAME]) + name.encode('utf-8')
    
    adv_data = (
        bytes([len(flags_data)]) + flags_data + 
        bytes([len(name_data)]) + name_data
    )
    
    return adv_data

adv_data = create_advertising_data(device_name)

ble = ubluetooth.BLE()
ble.active(True)

def start_advertising():
    print(f"Запуск маяка с именем: {device_name}")
    ble.gap_advertise(100000, adv_data=adv_data) 

start_advertising()

try:
    while True:
        utime.sleep(1) 
except KeyboardInterrupt:
    print("Остановка маяка")
    ble.active(False) 