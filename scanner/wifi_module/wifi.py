import machine
import sys
import network
import time
import urequests
import ntptime

# Pin definitions
repl_button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
repl_led = machine.Pin(5, machine.Pin.OUT)

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if wlan.isconnected():
        print("Уже было подключено, сетевые настройки:", wlan.ifconfig())
    wlan.connect(ssid, password)
    max_wait = 10
    while max_wait > 0:
        if wlan.isconnected():
            break
        print('Ожидание подключения...', max_wait)
        time.sleep(1)
        max_wait -= 1

    if wlan.isconnected():
        print('Подключено, сетевые настройки:', wlan.ifconfig())
    else:
        print('Не удалось подключиться.')

    return wlan


def sync_time():
    try:
        print("Синхронизация времени с NTP...")
        ntptime.settime()
        print("Время синхронизировано")
        return True
    except Exception as e:
        print(f"Ошибка синхронизации времени: {e}")
        return False


def get_example(state):
    # Web page (non-SSL) to get
    url = "http://example.com"

    # Continually print out HTML from web page as long as we have a connection
    if state.isconnected():

        # Perform HTTP GET request on a non-SSL web
        response = urequests.get(url)

        # Display the contents of the page
        print(response.status_code)
    else:
        raise RuntimeError(f"No WiFi connection")


def disconnect_wifi(wlan, disable_interface=True):
    """Безопасное отключение WiFi с освобождением ресурсов

    Args:
        wlan: Объект WLAN
        disable_interface: Полное отключение интерфейса (освобождает UART)
    """
    try:
        if wlan.isconnected():
            print("Отключаем WiFi...")
            wlan.disconnect()
            time.sleep(0.5)  # Даём время на разрыв соединения

        if disable_interface:
            wlan.active(False)
            print("WiFi интерфейс деактивирован")

        return True
    except Exception as e:
        print(f"Ошибка отключения: {e}")
        return False