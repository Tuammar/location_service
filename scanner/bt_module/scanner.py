import time
import bluetooth
from micropython import const
from .adv_data_parser import parse_name_from_adv_data


_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)


def bt_irq(event, data):
  
  if event == _IRQ_SCAN_RESULT:
    # A single scan result.
    addr_type, addr, connectable, rssi, adv_data = data

    formatted_addr = ':'.join(['%02X' % i for i in addr])
    print(addr_type, formatted_addr, connectable, rssi)
    name = parse_name_from_adv_data(adv_data)
    print(name)
    if name.startswith('cu'):
        print("HERE")
  elif event == _IRQ_SCAN_DONE:
    # Scan duration finished or manually stopped.
    print('scan complete')

# Scan for 10s (at 100% duty cycle)
def start_listening(ms_scan=3000):
    bt = bluetooth.BLE()
    bt.irq(bt_irq)
    bt.active(True)
    bt.gap_scan(ms_scan, 30000, 30000)
    time.sleep_ms(ms_scan)
