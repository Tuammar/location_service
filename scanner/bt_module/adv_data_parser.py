from micropython import const
import json

AD_TYPE_COMPLETE_LOCAL_NAME = const(0x09)

def parse_name_from_adv_data(adv_data):
    i = 0
    result = {}
    mv = memoryview(adv_data)
    while i < len(mv):
        length = mv[i]
        if length == 0:
            break
        ad_type = mv[i + 1]
        data = bytes(mv[i + 2 : i + 1 + length])
        result[ad_type] = data
        i += 1 + length
    name_bytes = result.get(AD_TYPE_COMPLETE_LOCAL_NAME, b'')
    name = name_bytes.decode('utf-8') if name_bytes else "Unknown"
    return name

def parse_adv_data(adv_data):
    i = 0
    result = {}
    mv = memoryview(adv_data)
    block_names = ['flags', 'beacon_name', 'tx_power']
    block_index = 0
    
    while i < len(mv) and block_index < len(block_names):
        length = mv[i]
        if length == 0:
            break

        data = bytes(mv[i + 2 : i + 1 + length])
        

        if block_index == 1:  # device_name
            result['beacon_name'] = data.decode('utf-8')
        elif block_index == 2:  # tx_power
            if len(data) > 0:
                tx_power_raw = data[0]
                if tx_power_raw > 127:
                    tx_power = tx_power_raw - 256  # преобразуем в signed
                else:
                    tx_power = tx_power_raw
                result['tx_power'] = tx_power
        
        i += 1 + length
        block_index += 1
    
    return result