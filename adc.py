import RPi.GPIO as GPIO
import time
import numpy as np

# initialisation
dinPin = 11
doutPin = 22
clkPin = 15
csPin = 13

GPIO.setmode(GPIO.BOARD)

GPIO.setup(dinPin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(clkPin, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(csPin, GPIO.OUT, initial=GPIO.HIGH)

GPIO.setup(doutPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def get_address(bit_string):
     
     address_string=''
     
     for i, digit in enumerate(bit_string):
          if i>0 and i<4:
               address_string += digit

     return voltage

def get_voltage(bit_string, range_mode='1'):
     
     maxV=2.5

     binary_voltage=''

     if range_mode == '0':
          maxV=5.
          
     for i, digit in enumerate(bit_string):
          if i>3 and i<12:
               binary_voltage += digit

     voltage = (float(int(binary_voltage, 2))/256.)*maxV
               
     return voltage
    
def ADC(adc_channel, write_mode='1', sequence='1', shadow='1', range_mode='1', coding='1'):

     maxvoltage = 0.

     if range_mode == '1':
          maxvoltage=2.5
     else:
          maxvoltage=5

    #if not (maxvoltage >= voltage >= 0):
    #    print 'using voltages outside of range - I will wrap around!'
    

     # channel is set by the three address bits - address is simply
     # the binary equivalent of the channel number
     address = ''
     address = '{0:03b}'.format(int( adc_channel))
    
     # we need to define the control register before writing or reading
     # anything. This is 
     # |write|seq|DC|ADD2|ADD1|ADD0|PM1|PM0|shadow|DC|range|coding
     # The default values set all bits to 1 for a dummy conversion.
     # Don't care bits can be anything, so we set them to 1 for default
     # dummy conversions. We must write 16 bits, but only 12 are read, so
     # again we set the final 4 bits to 1.
     control_register = write_mode + sequence + '1' + address + '11' + shadow + '1' + range_mode + coding + '1111'

     # create a private variable to store the conversion
     digital_conversion = ''

     # drop CS to low to prepare the chip to read SDI pin
     GPIO.output(csPin,0)
     
     # Control is written to the register on falling edge. So raise the
     # clock, put a digit on the feed line and drop the clock. Conversions
     # are clocked out onto the DOUT pin on the same falling edge.
     for digit in control_register:

          # read the digital output
          if GPIO.input(doutPin):
               digital_conversion += '1'
          else:
               digital_conversion += '0'                
    
          # place a digit on the feed line
          GPIO.output(dinPin, int(digit))
          
          # clock the digit into the control register
          GPIO.output(clkPin,0)
                    
          # raise the clock again ready for the next cycle
          GPIO.output(clkPin,1)

     GPIO.output(csPin,1)
     
     return digital_conversion

channel_number = 0

ADC(channel_number)
ADC(channel_number)
ADC(channel_number, write_mode='1', sequence='0', shadow='0', range_mode='0')

for i in range(1,10):
     print get_voltage(ADC(channel_number, write_mode='0', sequence='0', shadow='0', range_mode='0'),range_mode='0')

GPIO.cleanup()
