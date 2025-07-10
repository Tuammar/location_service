update: upload_main upload_wifi upload_bluetooth connect
	
upload_bluetooth:
	mpremote fs mkdir bt_module || true
	mpremote fs cp bt_module/__init__.py :bt_module/
	mpremote fs cp bt_module/adv_data_parser.py :bt_module/
	mpremote fs cp bt_module/lighthouse.py :bt_module/
	mpremote fs cp bt_module/scanner.py :bt_module/

upload_wifi:
	mpremote fs mkdir wifi_module || true
	mpremote fs cp wifi_module/__init__.py :wifi_module/
	mpremote fs cp wifi_module/wifi.py :wifi_module/

upload_main:
	mpremote fs cp main.py :

connect:
	mpremote connect auto

ls:
	mpremote fs ls