#!/usr/bin/env python
#
# Read DS18B20 1-wire temp sensors and output Fahrenheit
# 

import os, sys

def find_sensors(basedir):
    return [x for x in os.listdir(basedir) if x.startswith('28')]


def read_temp(sensor):
    with open(sensor + '/w1_slave', "r") as f:
        data = f.readlines()

    if data[0].strip()[-3:] == "YES":
        return [True, float(data[1].split("=")[1])]
    else:
        return [False, 0.0]


def celsius_to_fahrenheit(c):
    return (c * 1.8) + 32.0


if __name__ == "__main__":

    basedir = '/sys/bus/w1/devices'

    sensors = find_sensors(basedir)

    if not sensors:
        print "No sensors found"
        sys.exit(0)

    for s in sensors:
        (ok, temp) = read_temp(basedir + '/' + s)

        if ok:
            print s, ': Raw', temp, ' Fahrenheit', celsius_to_fahrenheit(temp / 1000.0)
        else:
            print s, ': Sensor not ready for reading'

