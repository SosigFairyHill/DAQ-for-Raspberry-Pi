import RPi.GPIO as GPIO
import time
import numpy as np

# initialisation
adc_dinPin = 11
adc_doutPin = 22
dac_sdiPin = 16
clkPin = 15
adc_csPin = 13
dac_csPin = 18


GPIO.setmode(GPIO.BOARD)

GPIO.setup(adc_dinPin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(dac_sdiPin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(clkPin, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(adc_csPin, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(dac_csPin, GPIO.OUT, initial=GPIO.HIGH)

GPIO.setup(adc_doutPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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
    
def twoway(adc_channel, dac_channel, output_voltage, write_mode='1', sequence='1', shadow='1', range_mode='1', coding='1'):

     maxvoltage = 0.

     if range_mode == '1':
          maxvoltage=2.5
     else:
          maxvoltage=5

     if not (maxvoltage >= voltage >= 0):
         print 'using voltages outside of range!'
    

     # adc channel is set by the three address bits - address is
     # the binary equivalent of the channel number
     adc_address = ''
     adc_address = '{0:03b}'.format(int( adc_channel))

     # dac channel the same but 4 bit
     dac_address = ''
     dac_address = '{0:04b}'.format(int( dac_channel))

     output_value = '{0:08b}'.format(int( (255*(float(output_voltage)/float(maxvoltage))) ))
    
     # we need to define the control register before writing or reading
     # anything. This is 
     # |write|seq|DC|ADD2|ADD1|ADD0|PM1|PM0|shadow|DC|range|coding
     # The default values set all bits to 1 for a dummy conversion.
     # Don't care bits can be anything, so we set them to 1 for default
     # dummy conversions. We must write 16 bits, but only 12 are read, so
     # again we set the final 4 bits to 1.
     adc_control_register = write_mode + sequence + '1' + address + '11' + shadow + '1' + range_mode + coding + '1111'

     dac_control_register = dac_address + output_value

     # create a private variable to store the conversion
     digital_conversion = ''

     # drop CS to low to prepare the chip to read SDI pin
     GPIO.output(adc_csPin,0)
     GPIO.output(dac_csPin,0)
     
     # Control is written to the register on falling edge. So raise the
     # clock, put a digit on the feed line and drop the clock. Conversions
     # are clocked out onto the DOUT pin on the same falling edge.
     for i, digit in enumerate(adc_control_register):

          # read the digital output
          if GPIO.input(adc_doutPin):
               digital_conversion += '1'
          else:
               digital_conversion += '0'                
    
          # place a digit on the ADC feed line
          GPIO.output(adc_dinPin, int(digit))
          
          # clock the digit into the ADC control register
          GPIO.output(clkPin,0)

          # place a digit on the DAC feed line
          GPIO.output(dac_sdiPin, int(dac_control_register[i]))
                    
          # raise the clock again to clock in the DAC bit and get
          # ready for the next cycle
          GPIO.output(clkPin,1)
          
          # after 12 bits the dac cs pin must be raised high (once the
          # clock is high)
          if i>11:
              GPIO.output(dac_csPin,1)

     GPIO.output(adc_csPin,1)
     
     return digital_conversion

adc_channel = 0
volts_out = 2.
dac_channel = 0 
twoway(adc_channel, dac_channel, volts_out)
twoway(adc_channel, dac_channel, volts_out)
twoway(adc_channel, dac_channel, volts_out, write_mode='1', sequence='0', shadow='0', range_mode='0')

for i in range(1,10):
     print get_voltage(twoway(adc_channel, dac_channel, volts_out, write_mode='0', sequence='0', shadow='0', range_mode='0'),range_mode='0')

GPIO.cleanup()
