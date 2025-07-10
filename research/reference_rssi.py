import time
import bt
from micropython import const


_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)

# TARGET_ADDR = "E8:FF:F4:4B:24:18" # айфон
# TARGET_ADDR = "74:15:75:D6:54:C4" # poco
TARGET_ADDR = "88:6B:6E:F3:EF:6A" # beats
# TARGET_ADDR = "14:3A:9A:0B:63:7E" # dualsence
# TARGET_ADDR = "AC:80:FB:87:99:31" # buds fe


def bt_irq(event, data):
  
  if event == _IRQ_SCAN_RESULT:
    # A single scan result.
    addr_type, addr, connectable, rssi, adv_data = data

    formatted_addr = ':'.join(['%02X' % i for i in addr])
    # if formatted_addr == TARGET_ADDR:
    print(rssi)

    # else:
    #   print(formatted_addr)
    # b_adv_data = bytes(adv_data)
    # print(b_adv_data)
    # print(b_adv_data[0])
    # print(b_adv_data[1])
    # print(b_adv_data[2:])
  elif event == _IRQ_SCAN_DONE:
    # Scan duration finished or manually stopped.
    print('scan complete')

# Scan for 10s (at 100% duty cycle)
ms_scan = 0
bt = bt.BLE()
bt.irq(bt_irq)
bt.active(True)
print("START LISTENING")
bt.gap_scan(ms_scan, 30000, 30000)
time.sleep_ms(ms_scan)