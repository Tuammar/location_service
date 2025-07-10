from bt_module.scanner import start_listening
from wifi_module.wifi import connect_to_wifi, get_example

# Network settings
WIFI_SSID = "TITANS"
WIFI_PASSWD = "DORADURA"

start_listening()

wifi_state = connect_to_wifi(WIFI_SSID, WIFI_PASSWD)
get_example(wifi_state)
