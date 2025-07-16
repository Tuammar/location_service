import time
import bluetooth
from micropython import const
from .adv_data_parser import parse_name_from_adv_data, parse_adv_data
from .mqtt_module import connect_mqtt, disconnect_mqtt, send_message


_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)

_mqtt_state = None


def bt_irq(event, data):
  scanner_name = "cu_P_scanner"

  
  if event == _IRQ_SCAN_RESULT:
    # A single scan result.
    addr_type, addr, connectable, rssi, adv_data = data

    formatted_addr = ':'.join(['%02X' % i for i in addr])
    name = parse_name_from_adv_data(adv_data)
    if name.startswith('cu'):
        message = parse_adv_data(adv_data)
        message["mac"] = formatted_addr
        message["timestamp"] = time.time()
        message["rssi"] = rssi
        message["scanner_name"] = scanner_name

        if _mqtt_state is not None:
            send_message(_mqtt_state, message)

  elif event == _IRQ_SCAN_DONE:
    # Scan duration finished or manually stopped.
    print('scan complete')

# Scan for 10s (at 100% duty cycle)
def start_listening(ms_scan=3000):
    print('start listening...')

    global _mqtt_state
    _mqtt_state = connect_mqtt()
    
    bt = bluetooth.BLE()
    bt.irq(bt_irq)
    bt.active(True)
    bt.gap_scan(ms_scan, 30000, 30000)
    time.sleep_ms(ms_scan)
    if _mqtt_state is not None:
        disconnect_mqtt(_mqtt_state)
