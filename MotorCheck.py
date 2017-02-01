# Script that controls 2 DC motors on a Billy Bass Fish
# Based on the Adafruit DCTest.py script 
# Author: Mari DeGrazia
# arizona4n6@gmail.com

import time
import atexit
from multiprocessing import Process
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

MOTOR_HEAD_TAIL = 1
MOTOR_MOUTH = 2

#function to tilt head up when the fish talks
def head_tilt():
	while True:
		myMotorHead.run(Adafruit_MotorHAT.BACKWARD)
		time.sleep(60)
		myMotorHead.run(Adafruit_MotorHAT.RELEASE)

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
		print "This will test the Billy Bass motors"
		print "The head will tilt up, and the mouth should move several times"
		p = Process(target=head_tilt)
		p.start()

		for x in range(0,4):
		
			#move the mouth
			myMotorMouth.run(Adafruit_MotorHAT.BACKWARD)
			time.sleep(1)
			myMotorMouth.run(Adafruit_MotorHAT.RELEASE)
			time.sleep(1)
		p.terminate()
		
		print "Test Complete"
		


