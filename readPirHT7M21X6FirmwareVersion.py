#!/usr/bin/python2

from smbus2 import SMBus # import library smbus2 compatible to use I2C
bus = SMBus(1)
a = bus.read_i2c_block_data(0x4c,10,2) # go read the firmware version

major = format(a[0],'02x') # high byte
minor = format(a[1],'02x') # low byte

print ("Pir sensor firmware version is : " + major +"."+ minor) # display the value
