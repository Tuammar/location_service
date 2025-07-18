update_scanner: upload_wifi upload_bluetooth upload_mqtt upload_main connect
	
upload_bluetooth:
	mpremote fs mkdir bt_module || true
	mpremote fs cp scanner/bt_module/__init__.py :bt_module/
	mpremote fs cp scanner/bt_module/adv_data_parser.py :bt_module/
	mpremote fs cp scanner/bt_module/scanner.py :bt_module/

upload_wifi:
	mpremote fs mkdir wifi_module || true
	mpremote fs cp scanner/wifi_module/__init__.py :wifi_module/
	mpremote fs cp scanner/wifi_module/wifi.py :wifi_module/

upload_mqtt:
	mpremote fs mkdir bt_module/mqtt_module || true
	mpremote fs cp scanner/bt_module/mqtt_module/__init__.py :bt_module/mqtt_module/
	mpremote fs cp scanner/bt_module/mqtt_module/mqtt_client.py :bt_module/mqtt_module/
	mpremote fs cp scanner/bt_module/mqtt_module/umqtt_simple.py :bt_module/mqtt_module/


upload_main:
	mpremote fs cp scanner/main.py :

update_beacon:
	mpremote fs cp beacon/main.py :main.py

connect:
	mpremote connect auto

ls:
	mpremote fs ls
