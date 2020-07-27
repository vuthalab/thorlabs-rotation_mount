'''
Code for the ELL14K Rotation Mount
July, 23 2020, Sarina Xi. University of Toronto
'''
​
import serial
import numpy as np
import time
​
#Note that unreasonably large or small angles of rotation will break the program.
class ELL14K:
    FACTOR = 398.23 #factor of ratio to transform the degree to a hexadecimal value
    def __init__(self,address='/dev/ttyUSB0'):
        self.mount = serial.Serial(address,baudrate=9600,stopbits=1,parity='N',timeout = 0.1)
​
    def writes(self, command):
        self.mount.write(command.encode())
​
    def read(self):
        return self.mount.readlines()
​
    def home(self):
        self.writes('0ho3\n')
​
    def get_motor_para(self):
        self.writes('0i1\n')
        message = str(self.read())
        fwP = message[20:24] #forward period
        bwP = message[24:28] #backwards period
        #frequncy = 14740000/period page 13 on communication protocal
        decf = round(14740/int('0x'+fwP, 0), 1) #kHz
        decb = round(14740/int('0x'+bwP, 0), 1) #kHz
        print(decf, decb)
        #return self.read()
​
    def set_forward_f(self, freq):
        period = int(14740/freq)
        message = hex(period).upper()
        self.writes('0f100'+message[2:]+'\n')
​
    def set_backward_f(self, freq):
        period = int(14740/freq)
        message = hex(period).upper()
        self.writes('0b100'+message[2:]+'\n')
​
​
    def jog_forward(self, degree):
        self.set_rotation_degree(degree)
        self.writes('0fw\n')
        return self.read()
​
    def jog_backward(self, degree):
        self.set_rotation_degree(degree)
        self.writes('0bw\n')
        return self.read()
​
    def set_rotation_degree(self, degree):
        val = round(degree*device.FACTOR)
        use = str(hex(val)).upper()
        #the following angles are gotten by transforming hexadecimal limit to degrees
        if degree < 10.28:
            message = "0sj00000"+use[2:]+"\n"
        if degree >10.28 and degree < 164.52:
            message = "0sj0000"+use[2:]+"\n"
        if degree >164.52 and degree < 2632.5:
            message = "0sj000"+use[2:]+"\n"
​
        self.writes(message)
        return self.read()
​
    def get_position(self):
        self.writes('0gp\n')
        message = self.read()
        hexa = str(message)[9:14]
        if hexa[0]==0 and hexa[1]==0:
            dec = int("0x"+hexa[2:], 0)
        if hexa[0]==0 and hexa[1]!=0:
            dec = int("0x"+hexa[1:], 0)
        if hexa[0]!=0:
            dec = int("0x"+hexa[:], 0)
        if hexa[:-1] == "FFFF":
            dec = 0
        return round(dec/device.FACTOR, 1)
​
    def get_jogsize(self):
        self.writes('0gj\n')
        message =  self.read()
        hexa = str(message)[8:13]
        dec = int("0x"+hexa, 0)
        return round(dec/device.FACTOR, 1)
​
    def set_angle(self, degree):
        position = self.get_position()
        diff = degree - position
        if diff > 0:
            self.jog_forward(diff)
        if diff < 0:
            self.jog_backward(0-diff)
​
    def close(self):
        self.mount.close()
        print("Bye")
​
'''
device = ELL14K()
for i in range(50):
    device.jog_forward(90)
    time.sleep(0.5)
    device.jog_backward(90)
    time.sleep(0.5)
    print(i)
'''
​
