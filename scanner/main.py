from bt_module.scanner import start_listening
from bt_module.rssi_reference import start_listening_rssi
from wifi_module.wifi import connect_wifi, get_example, disconnect_wifi

# Network settings
WIFI_SSID = "TITANS"
WIFI_PASSWD = "DORADURA"

wifi_state = connect_wifi(WIFI_SSID, WIFI_PASSWD)
get_example(wifi_state)

start_listening()

disconnect_wifi(wifi_state)
