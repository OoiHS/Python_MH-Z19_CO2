'''
You need to enable Serial port in RaspberryPi first:
- Run RaspberryPi Terminal
- sudo raspi-config
-  Interface Options
-  Serial Port
-  Would you like the serial port hardware to be enabled? [YES]
-  Accept and reboot RaspberryPi.
'''

import serial
import time

ser = serial.Serial('/dev/serial0', 9600) #ttyAMA0


while True:
    ser.write(b"\xff\x01\x86\x00\x00\x00\x00\x00\x79")
    time.sleep(2)
    response = ser.read(9)
    print(response)
    if response[0] == ord("\xff") and response[1] == ord("\x86"):
        print( response[2]*256 + response[3] )

ser.close()

def crc8(a):
    crc=0x00
    count=1
    b=bytearray(a)
    while count<8:
        crc+=b[count]
        count=count+1
    #Truncate to 8 bit
    crc%=256
    #Invert number with xor
    crc=~crc&0xFF
    crc+=1
    return crc


z = bytearray(response)
crc=crc8(response)
#Calculate crc
if crc != z[8]:
    print("Corrupted Value")
else:
    print("ALL GOOD")

