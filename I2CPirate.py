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

ser = serial.Serial(
    port='COM8',
    baudrate=115200
)

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
    while x <= 30:
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
        
            
while 1:
    print("UMIDADE")
    print(read_humidity())
    print("TEMPERATURA")
    print(read_temperature())
    time.sleep(30)