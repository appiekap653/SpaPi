"""Read temperture values from DS18B20"""
import glob
from spapi import gpio_controller

def read_temp_raw(sensor_file):
    sfile = open(sensor_file, 'r')
    lines = sfile.read()
    sfile.close()
    return lines

def read_temp() -> float:
    _temp_controller = gpio_controller.Controllers.thermometercontroller()

    for sensor in glob.glob("/sys/bus/w1/devices/w1_bus_master1/28-*/w1_slave"):
        try:
            data = read_temp_raw(sensor)

            if "YES" in data:
                (discard, sep, reading) = data.partition(' t=')
                temp_c = float(reading) / 1000.0
                return temp_c
            return 999.9
        except:
            pass
