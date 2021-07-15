'''
You need to enable Serial port in RaspberryPi first:
> Run RaspberryPi Terminal
> sudo raspi-config
   Interface Options
   Serial Port
   Would you like the serial port hardware to be enabled? [YES]
   Accept and reboot RaspberryPi.

https://www.programmersought.com/article/92047061453/
https://www.raspberrypi.org/documentation/configuration/uart.md
These will enable the additional UART pins that was hidden (only for RaspberryPi 4 and above)
> ls /dev/ttyAMA*		[You should see only a few UART is up]
> sudo nano /boot/config.txt
   dtoverlay=uart1
   dtoverlay=uart2
   dtoverlay=uart3
   dtoverlay=uart4
   dtoverlay=uart5
   # dtoverlay=uart1,txd1_pin=32,rxd1_pin=33
> reboot
> ls /dev/ttyAMA*		[You should now see more UART is up]
> dtoverlay -h uart1		Shows some description for GPIO UART pins


GPIO14 = TXD0 -> ttyAMA0
GPIO15 = RXD0 -> ttyAMA0

GPIO0  = TXD2 -> ttyAMA1
GPIO1  = RXD2 -> ttyAMA1

GPIO4  = TXD3 -> ttyAMA2
GPIO5  = RXD3 -> ttyAMA2

GPIO8  = TXD4 -> ttyAMA3
GPIO9  = RXD4 -> ttyAMA3

GPIO12 = TXD5 -> ttyAMA4
GPIO13 = RXD5 -> ttyAMA4
'''

import serial
import time

ser = serial.Serial('/dev/serial0', 9600) #serial0, ttyAMA1, ttyAMA2


while True:
    ser.write(b"\xff\x01\x86\x00\x00\x00\x00\x00\x79")
    time.sleep(5)
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

