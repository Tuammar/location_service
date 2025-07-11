import time
import bluetooth
from micropython import const
from .adv_data_parser import parse_name_from_adv_data

_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)

TARGET_NAME = "cu_tralalelo"
LOG_FILE = f"rssi_{TARGET_NAME}_scan.csv"

def bt_irq(event, data):
    if event == _IRQ_SCAN_RESULT:
        # A single scan result.
        addr_type, addr, connectable, rssi, adv_data = data

        formatted_addr = ':'.join(['%02X' % i for i in addr])
        name = parse_name_from_adv_data(adv_data)
        if name == TARGET_NAME:
            print(rssi)
            # with open(LOG_FILE, "a") as f:
            #     f.write(f"{rssi}")
    elif event == _IRQ_SCAN_DONE:
        # Scan duration finished or manually stopped.
        print('scan complete')


# Scan for 10s (at 100% duty cycle)
def start_listening_rssi(ms_scan=180000):
    bt = None
    try:
        bt = bluetooth.BLE()
        bt.irq(bt_irq)
        bt.active(True)
        bt.gap_scan(ms_scan, 30000, 30000)
        time.sleep_ms(ms_scan)
    except Exception as e:
        print(f"Scan error: {e}")
    finally:
        if bt:
            bt.active(False)  # Гарантированное отключение
            print("Bluetooth deactivated")
