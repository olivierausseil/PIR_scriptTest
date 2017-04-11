#!/usr/bin/python2

from smbus2 import SMBus
bus = SMBus(1)


choice = input("You want read(type 1) or modify the value? ")

if (choice ==1)
{
    readValue = bus.read_i2c_block_data(0x4c,2,2)
    major = format(readValue[0],'02x')
    #minor = format(a[1],'02x')

    print (" the Brightness is : " + major )
}
else
{
     valueOfBrightness = input("Enter a value between 0 and 127 ")
     data = [valueOfBrightness,0x98]
     bus.write_i2c_block_data(0x4c, 0, data)

}


#data = [1, 2, 3, 4, 5, 6, 7, 8]
#bus.write_i2c_block_data(80, 0, data)
