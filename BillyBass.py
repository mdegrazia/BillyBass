# Script that syncs two motors on Billy Bass to noise from a sensor
# Sensor/SPI code based on an example from  http://www.instructables.com/id/Dog-Bark-Sensor/step3/Software/
# DC Motor code based on an example from Adafruit DCTest.py script https://github.com/adafruit/Adafruit-Motor-HAT-Python-Library
# Author: Mari DeGrazia

import time
import spidev
import atexit
from multiprocessing import Process
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

MOTOR_HEAD_TAIL = 1
MOTOR_MOUTH = 2

#Pedometer value for the sound sensor. Adjust down if the mouth is moving too much, or up if the mouth is not moving enough
SENSITIVITY = 1000
#controls how long the head will stay tilted up. 
HEAD_PAUSE = 30000


# Establish SPI device on Bus 0, Device 0
spi = spidev.SpiDev()
spi.open(0,0)

def getAdc (channel):
	#check for valid channel
	if ( (channel > 7) or (channel < 0) ):
		return -1

	# Preform SPI transaction and store returned bits in 'r'
	r = spi.xfer( [1, (8 + channel) << 4, 0] )


	# Filter data bits from returned bits
	adcOut = ( (r[1] & 3) << 8 ) + r[2]

	# If adcOut is greater than 700 send a text via email through terminal
	return adcOut


#function to tilt head up when the fish talks
def head_tilt():
	while True:
		myMotorHead.run(Adafruit_MotorHAT.BACKWARD)
		#time.sleep(60)

				# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(MOTOR_HEAD_TAIL).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(MOTOR_MOUTH).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)	

#set up motors
mh = Adafruit_MotorHAT(addr=0x60)

myMotorMouth = mh.getMotor(MOTOR_MOUTH)
myMotorMouth.setSpeed(255)
myMotorMouth.run(Adafruit_MotorHAT.RELEASE)

myMotorHead =  mh.getMotor(MOTOR_HEAD_TAIL)
myMotorHead.setSpeed(255)
myMotorHead.run(Adafruit_MotorHAT.RELEASE)

if __name__ == '__main__':
	count = 0
	process_started = False

	print "Starting Billy Bass sound monitoring..."
	while True:
       
		adcOut = getAdc(0)
		
		#make the mouth move if sensitivity is over certain number
		if (adcOut > SENSITIVITY):
			count = 0
		
			myMotorMouth.run(Adafruit_MotorHAT.BACKWARD)
			time.sleep(.1)
			myMotorMouth.run(Adafruit_MotorHAT.RELEASE)

			#tilt the head out if the talking just started
			if process_started == False:
				process_started = True
				p = Process(target=head_tilt)
				p.start()

		
		else:
			#keep track of the pauses between words to find out when the talking stops to lower the head
			if process_started == True:
				count = count +1
				if count > HEAD_PAUSE:
					p.terminate()
					myMotorHead.run(Adafruit_MotorHAT.RELEASE)
					
					#when Billy Bass's head lowers,it hits mount right above the speaker
					#this causes the sensor to register enough sound to lift the head up again.
					#We need to pause the script to give enough time for his head to lower before checking for noise again
					time.sleep(3)
					count = 0
					process_started = False

