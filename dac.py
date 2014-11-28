import RPi.GPIO as GPIO
import time
import numpy as np

# initialisation
sdiPin = 13
clkPin = 11
csPin = 16

GPIO.setmode(GPIO.BOARD)
GPIO.setup(sdiPin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(clkPin, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(csPin, GPIO.OUT, initial=GPIO.HIGH)
    
def DAC(dac_channel,voltage):

     maxvoltage = 4.67

    #if not (maxvoltage >= voltage >= 0):
    #    print 'using voltages outside of range - I will wrap around!'
    

     # channel is set by the first four address bits - address is simply
     # the binary equivalent of the channel number
     address = ''
     address = '{0:04b}'.format(int( dac_channel))
    
     # reformat value to 8bit binary string
     value = '{0:08b}'.format(int( (255*(float(voltage)/float(maxvoltage))) % 256 ))
    
     # address byte preceeds value byte
     word = address + value
    
     # drop CS to low to prepare the chip to read SDI pin
     GPIO.output(csPin,0)
     GPIO.output(clkPin,0)
     # put our digit on the feed line, then clock the strobe line
     for digit in word:
          GPIO.output(sdiPin,int(digit))
          # clocked on rising edge
          GPIO.output(clkPin,1)
          GPIO.output(clkPin,0)
          
     GPIO.output(clkPin,1)
     GPIO.output(csPin,1)
  
DAC(0, 2.32)
time.sleep(1)

GPIO.cleanup()
