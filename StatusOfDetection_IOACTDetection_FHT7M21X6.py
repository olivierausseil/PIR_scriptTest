#!/usr/bin/python2
# ----------------- Initialization --------------------
#library import
import time
import logging
import sys
import argparse
import RPi.GPIO as GPIO

timeDetection = 0
endTimeDetection = 0
detection = 0
flagTime = 0
loopInfinite = True
maxbyte = 65535 #maximum value to 2 bytes

#GPIO initialization
ledPin = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.IN)

#recover the date and hour, choose the format to acquisition
#FORMAT = '%(asctime)s %(message)s',datefmt='%a %d %b %Y %H:%M:%S'
logging.basicConfig(level = logging.INFO,
                    format= '%(asctime)s %(message)s',
                    datefmt='%a %d %b %Y %H:%M:%S')

#Initilization of I2C bus
from smbus2 import SMBus
bus = SMBus(1)

#test on a bit who is interesting -> Method
def testBit(int_type, offset):
   mask = 1 << offset
   return(int_type & mask)

# -------------- End of initialization ----------------

# -----  parser ----- do arguments when we launch the script
parser = argparse.ArgumentParser()
parser.add_argument('-sT', action='store', dest='sensitivityTrigger')
parser.add_argument('-sG', action='store', dest='sensitivityGain')
parser.add_argument('-t', action='store', dest='triggerTime')

results = parser.parse_args()

#------- Sensitivity --------
# in case argument has not been provided
if None == results.sensitivityGain:
    sensitivityGain = int(16)
else:
    sensitivityGain = int(results.sensitivityGain)

# manage argument limits (0-31) because 5 bits allow (see datasheet_HT7Mx6 __ p12 _ 1. Sensor Config Register)
if sensitivityGain < 0:
    sensitivityGain = 0

if sensitivityGain > 31:
    sensitivityGain = 31

# from there, sensitivity takes a value between 0 and 31 in all cases
print ("sensitivity Gain is: " + str(sensitivityGain) )



if None == results.sensitivityTrigger:
    sensitivityTrigger = int(0)
else:
    sensitivityTrigger = int(results.sensitivityTrigger)

# manage argument limits (0-7) because 3 bits allow (see datasheet_HT7Mx6 __ p12 _ 1. Sensor Config Register)
if sensitivityTrigger < 0:
    sensitivityTrigger = 0

if sensitivityTrigger > 7:
    sensitivityTrigger = 7


# from there, sensitivity takes a value between 0 and 7 in all cases
print ("sensitivity Trigger is: " + str(sensitivityTrigger) )

# sum of the two sensitivity
sensitivity = (sensitivityTrigger << 5) +  sensitivityGain

if sensitivityTrigger == 0 :
    sensitivity = sensitivityGain
if sensitivityGain == 0 :
    sensitivity = sensitivityTrigger
print sensitivity
#-------------- end sensitivity ---------

#---------------TriggerTime -------------
if None == results.triggerTime:
    triggerTime = int(50)
else:
    triggerTime = int(results.triggerTime)

if triggerTime < 0:
    triggerTime = 0

if triggerTime > maxbyte:
    triggerTime = maxbyte

# cut in two the data
triggerTimeMSB = triggerTime >> 8 # MSB
triggerTimeLSB = triggerTime & 0xFF # LSB

#triggerTime = int(triggerTime) * 10
#----------------end TriggerTIme --------
# -------------- end parser  ------------

time.sleep(0.1)

# change the trigger time of detection (see datasheet_HT7Mx6 __ p15 _ 3.Trig Time Interval )
data_time = bus.read_i2c_block_data(0x4c, 3, 2)
#print ( "data_time : " + str(data_time))
data_time[1] = triggerTimeLSB
data_time[0] = triggerTimeMSB

#print ( "data_time change : " + str(data_time))
bus.write_i2c_block_data(0x4c, 3, data_time)
print ( "trigger time  : " + str(data_time[1]))

time.sleep(0.1)

# change of trigger parameter (see datasheet_HT7Mx6 __ p12 _ 1. Sensor Config Register)

data = bus.read_i2c_block_data(0x4c, 1, 2)


data[1] = sensitivity
bus.write_i2c_block_data(0x4c, 1, data)
print ( "sensitivity: " + str(data[1]))


# read the value of the sensor when switch on detection or not
readValue = bus.read_i2c_block_data(0x4c,8,2)
readValue = map(int, readValue)

# ----- INITIAL TEST IN DETECTION -----------------
# testing the bit
detection = GPIO.input(ledPin)
print ''
if detection == 0 :
    print "Initial state of the sensor : \"no in detection\" "
    endTimeDetection = time.time()
else :
    print "Initial state of the sensor :  \"detection \"  "
    timeDetection = time.time()

print " Now, we enter to the test loop to see if an other detection occur\n "
#
while loopInfinite :
    detectionTemporary = GPIO.input(ledPin)
    # if the state is "No detection"
    if detection == 0 :
        if detection != detectionTemporary :
            # change of state
            #print("The sensor detects presence")
            timeDetection = time.time()
            detection = detectionTemporary
            logging.info(' : DETECTION !!!!!!')
            print ''
            #logging.info(' : The sensor detects a presence !')

    if detection != 0 :
        if detection != detectionTemporary :
            #print("End of the presence detection")
            endTimeDetection = time.time()
            detection = detectionTemporary
            logging.info(' : End of detection')
            flagTime = 1

    time.sleep(0.1)
    # for calculate the detection time
    if flagTime == 1 :
        finalTime = endTimeDetection - timeDetection
        print ("detection time : "+ "%.2f" % finalTime)
        print ''
        flagTime = 0
