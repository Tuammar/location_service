from micropython import const

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