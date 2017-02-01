# This script will check the adafruit MCP3800 and Adafruit Microphone Amplifier MAX4466
# Based on code from  http://www.instructables.com/id/Dog-Bark-Sensor/step3/Software/
# Author: Mari DeGrazia
# arizona4n6@gmail.com


import time
import spidev

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

print "Sound Sensor values...."
while True:
	adcOut = getAdc(0)
	print adcOut
	time.sleep(.5)


