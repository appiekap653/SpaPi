"""Read temperture values from DS18B20"""
import glob
import time
 
def read_temp_raw(sensor_file):
    f = open(sensor_file, 'r')
    lines = f.read()
    f.close()
    return lines
 
def read_temp():
    for sensor in glob.glob("/sys/bus/w1/devices/28-00*/w1_slave"):
        id = sensor.split("/")[5]

        try:
            data = read_temp_raw(sensor)

            if "YES" in data:
                (discard, sep, reading) = data.partition(' t=')
                temp_c = float(reading) / 1000.0
                return temp_c
            else:
                return "999"
        except:
            pass
