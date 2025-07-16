from micropython import const
import ubluetooth, utime

AD_TYPE_FLAGS = const(0x01)
AD_TYPE_COMPLETE_LOCAL_NAME = const(0x09)
AD_TYPE_TX_POWER_LEVEL = const(0x0A)

FLAGS_GENERAL_DISCOVERY = const(0x06)

device_name = "cu_P_beacon"
tx_power_level = -73 # RSSI на расстоянии 1 метра


def create_advertising_data(name, tx_power):
    flags_data = bytes([AD_TYPE_FLAGS, FLAGS_GENERAL_DISCOVERY])

    name_bytes = name.encode("utf-8")
    name_data = bytes([AD_TYPE_COMPLETE_LOCAL_NAME]) + name_bytes

    tx_power_data = bytes([AD_TYPE_TX_POWER_LEVEL, tx_power & 0xFF])

    adv_data = (
        bytes([len(flags_data)])
        + flags_data
        + bytes([len(name_data)])
        + name_data
        + bytes([len(tx_power_data)])
        + tx_power_data
    )
    return adv_data


adv_data = create_advertising_data(device_name, tx_power_level)

ble = ubluetooth.BLE()
ble.active(True)


def start_advertising():
    print(f"Запуск маяка с именем: {device_name}, TX Power: {tx_power_level} dBm")
    ble.gap_advertise(100000, adv_data=adv_data)


start_advertising()

try:
    while True:
        utime.sleep(1)
except KeyboardInterrupt:
    print("Остановка маяка")
    ble.active(False)
