import serial
import time

ser = serial.Serial(
    port='COM8',
    baudrate=115200
)


def I2C_init:
    ser.write(b"m\n\r")#enter in mode selection on bus pirate
    time.sleep(1)
    ser.write(b"4\n\r")#enter in I2C mode on bus pirate
    time.sleep(1)
    ser.write(b"1\n\r")#5khz on I2C velocity because we doesn't need more
    time.sleep(1)
    ser.write(b"P\n\r")#Enable Bus Pirate Power Supply
    time.sleep(1)

while 1:
    ser.write(b"[0x80 0xf5][0x81 r][0x81 r][0x81 rr]\n\r")
    time.sleep(1)
    decode = ""
    while 1:
        #ser.flush()
        data = ser.readline().decode('utf-8')
        #print(data)
        decode += data
        print(decode)
    print(decode)
    time.sleep(10)
    
    