"""Read temperture values from DS18B20"""
import glob
import time
import RPi.GPIO as GPIO

pull_up_set = 0

def read_temp_raw(sensor_file):
    f = open(sensor_file, 'r')
    lines = f.read()
    f.close()
    return lines
 
def read_temp() -> float:
    global pull_up_set
    if pull_up_set == 0:
        GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        pull_up_set = 1

    for sensor in glob.glob("/sys/bus/w1/devices/w1_bus_master1/28-*/w1_slave"):
        id = sensor.split("/")[5]

        try:
            data = read_temp_raw(sensor)

            if "YES" in data:
                (discard, sep, reading) = data.partition(' t=')
                temp_c = float(reading) / 1000.0
                return temp_c
            else:
                return 999.9
        except:
            pass
