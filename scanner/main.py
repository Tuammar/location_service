from bt_module.scanner import start_listening
from wifi_module.wifi import connect_wifi, get_example, disconnect_wifi, sync_time

# Network settings
WIFI_SSID = "TITANS"
WIFI_PASSWD = "DORADURA"

wifi_state = connect_wifi(WIFI_SSID, WIFI_PASSWD)


try:
    get_example(wifi_state)
    # Синхронизируем время с NTP сервером
    sync_time()

    # while True:
    start_listening(ms_scan=606456986)

finally:
    disconnect_wifi(wifi_state)
