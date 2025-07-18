def distance_calculator(rssi, tx_power=-69, path_loss_exponent=2.3):
    exponent = (tx_power - rssi) / (10 * path_loss_exponent)
    distance = 10**exponent
    return round(distance, 2)
