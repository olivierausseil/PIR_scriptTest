#!/usr/bin/python2

#library import
import time
tempsDetection = 0
tempsFinDetection = 0
detection = 0

from smbus2 import SMBus
bus = SMBus(1)

#conversion decimal en binaire
#def dec_to_bin(x):
#    return int(bin(x)[2:])

#test on a bit who is interesting -> Method
def testBit(int_type, offset):
   mask = 1 << offset
   return(int_type & mask)
# --- old for test if my code is true ---
# read the value of the sensor
#readValue = bus.read_i2c_block_data(0x4c,8,2)
#readValue = map(int, readValue)

# testing the bit
#detection = testBit(readValue[1],0)
#print (readValue)
#print (detection)
# -------------------------------------------

# Wait for detection
while detection == 0:
    readValue = bus.read_i2c_block_data(0x4c,8,2)
    readValue = map(int, readValue)
    detection = testBit(readValue[1],0)
    #print (readValue)
    #print (detection)
    time.sleep(0.1)
    if detection:
        temps = time.strftime("%H:%M:%S")
        tempsDetection = time.time()
        print("detection")
        print(temps)
        break

#Wait fot the end-detection
while detection != 0 :
    readValue = bus.read_i2c_block_data(0x4c,8,2)
    readValue = map(int, readValue)
    detection = testBit(readValue[1],0)

    #print (readValue)
    #print (detection)
    time.sleep(0.1)
    if detection == 0:
        temps = time.strftime("%H:%M:%S")
        tempsFinDetection = time.time()
        print("end detection")
        print(temps)
        break


tempsfinal = tempsFinDetection - tempsDetection
print ("detection time : "+ "%.2f" % tempsfinal)
# print ("%.2f" % tempsfinal)
