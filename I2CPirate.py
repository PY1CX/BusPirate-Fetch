"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
This is a small python software for reading the Humidity and Temperature
with a Si7006 and the Bus Pirate Hardware.

Author : Felipe Navarro
Date   : 12/20/2015

This software is part of my final project at the Electrical Engineering degree.


--------------------------------WARNING---------------------------------------
 
: In this version, to work you MUST configure the Bus Pirate by hand
I'm still working in it.
Process to configure the Bus Pirate, use the following commands:
m (to select what mode do you wanna use)
4 (select I2C bus option)
1 (I'm using 5Khz because I doesn't need more)


 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 THE SOFTWARE.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import serial
import time
from time import gmtime

ser = serial.Serial(
    port='COM8',
    baudrate=115200
)

index = 0 # index for reading the measurement index

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
read_humidity is a function to read the humidity with the Si7006 sensor
Author : Felipe Navarro
Date   : 12/20/2015
inputs : nothing
return : humidity list
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def read_humidity():
    decode = ""
    ser.write(b"[0x80 0xf5][0x81 r][0x81 r][0x81 rr]\n\r")
    time.sleep(1)
    x = 0
    while x <= 32:
        ser.flush()
        data = ser.readline(x).decode('utf-8')
        #print(decode)
        decode += data
        #print(data)
        x += 1
    return decode  

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
read_temperature is a function to read the temperature with the Si7006 sensor
The temperature read is from the previus Humidity conversion
Author : Felipe Navarro
Date   : 12/20/2015
inputs : nothing
return : humidity list
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def read_temperature():
    decode = ""
    ser.write(b"[0x80 0xE0][0x81 rr]\n\r")
    time.sleep(1)
    x = 0
    while x <= 23:
        ser.flush()
        data = ser.readline(x).decode('utf-8')
        #print(decode)
        decode += data
        #print(data)
        x += 1
    return decode

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
__________________This is the main loop of the Software______________________
Calls the read_humidity() and read_temperature functions, converts the value
to decimal and after to current humidity and temperature values. 
Author : Felipe Navarro
Date   : 12/20/2015
inputs : nothing
output : write into data.txt and prints on command line the Humidity and Tem
perature values.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        
            
while 1:
    index += 1 #increment the measurement index
    date = time.strftime("%d %b %Y %H:%M:%S", gmtime()) #date acquisition
    
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    The following block of code calls a conversion in the Si7006 and slice the
    data on the python
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""    
    
    humidity = read_humidity()
    #print(humidity) #debug code
    humidity_ack = humidity[290:293]
    humidity1 = humidity[278:280] + humidity[296:298]#First call
    humidity2 = humidity[288:290] + humidity[306:308]#all others
    #print(humidity1, " ", humidity2) #debug code    
    temperature = read_temperature()
    temperature_ack = temperature[164:167]
    temperature = temperature[152:154] + temperature[170:172]
    
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    The following block of code converts the data into readable content
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""     
    try:
        humidity = int(humidity2, 16)
    except:
        humidity = int(humidity1, 16)
        
    temperature = int(temperature, 16)
        
    humidity     = int(((humidity*125)/65536)-6)
    temperature = int(((float(temperature)*171.12)/65536)-46.85 )
    
    
    #print on the command line the humidity and temperature
    print(index, date, "U", humidity, "T", temperature)
    
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    The following block of code writes the content into a txt file
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""  
    file_data = str(index) + ',' + date + ',' + 'U' + ',' + str(humidity) + ',' + "T" + ',' + str(temperature) + '\n'
    file = open("data.txt", "a")
    file.write(file_data) 
    
    time.sleep(5) #time between conversions
    
    