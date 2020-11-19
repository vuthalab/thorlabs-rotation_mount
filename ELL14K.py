import numpy as np
import time
import os
os.chdir("/home/labuser/Desktop/googledrive/code/Samarium_control/Widgets/Objects")
from ThorlabsPM100 import ThorlabsPM100, USBTMC


inst = USBTMC(device="/dev/usbtmc6")
power_meter = ThorlabsPM100(inst=inst)
power_meter.sense.average.count = 100
power_dict = {}


#Note that unreasonably large or small angles of rotation will break the program.
class ELL14K:
    FACTOR = 398.23 #factor of ratio to transform the degree to a hexadecimal value
    def __init__(self,address='/dev/ELL14K'):
        self.mount = serial.Serial(address,baudrate=9600,stopbits=1,parity='N',timeout = 0.2)

    def writes(self, command):
        self.mount.write((command+'\n').encode())

    def read(self):
        return self.mount.readlines()

    def home(self):
        self.writes('0ho3')

    def get_motor_para(self):
        self.writes('0i1')
        message = str(self.read())
        fwP = message[20:24] #forward period
        bwP = message[24:28] #backwards period
        #frequncy = 14740000/period page 13 on communication protocal
        decf = round(14740/int('0x'+fwP, 0), 1) #kHz
        decb = round(14740/int('0x'+bwP, 0), 1) #kHz
        print(decf, decb)

    def set_forward_f(self, freq):
        period = int(14740/freq)
        message = hex(period).upper()
        self.writes('0f100'+message[2:])

    def set_backward_f(self, freq):
        period = int(14740/freq)
        message = hex(period).upper()
        self.writes('0b100'+message[2:])

    def jog_forward(self, degree):
        self.set_rotation_degree(degree)
        self.writes('0fw')
        return self.read()

    def jog_backward(self, degree):
        self.set_rotation_degree(degree)
        self.writes('0bw')
        return self.read()

    def set_rotation_degree(self, degree):
        val = round(degree*ELL14K.FACTOR)
        use = str(hex(val)).upper()
        if degree < 10.28:
            message = "0sj00000"+use[2:]
        elif degree >10.28 and degree < 164.52: #angles are gotten by transforming hexadecimal limit to degrees
            message = "0sj0000"+use[2:]
        elif degree >164.52 and degree < 2632.5:
            message = "0sj000"+use[2:]
        else:
            message = "0sj00000000\n"
        self.writes(message)
        return message, self.read()

    def get_position(self):
        self.writes('0gp')
        try:
            message = str(self.read())
        except IndexError:
            message = str(self.read())

        #print(message)

        if message[-11:-6] != '':
            hexa = message[-11:-6] #the other parts of the message are 0s and heading letters
            if hexa[0]==0 and hexa[1]==0:
                dec = int("0x"+hexa[2:], 0)
            if hexa[0]==0 and hexa[1]!=0:
                dec = int("0x"+hexa[1:], 0)
            if hexa[0]!=0:
                dec = int("0x"+hexa[:], 0)
            if hexa[:-1] == "FFFF":
                dec = 0
            return round(dec/ELL14K.FACTOR, 5)

    def set_angle(self, degree):
        position = self.get_position()
        time.sleep(0.3)
        if position is not None:
            diff = round(degree - position, 1)
            while diff > 0.1:
                self.jog_forward(diff)
                time.sleep(0.3)
                pos = self.get_position()
                time.sleep(0.3)
                print(pos)
                if pos is not None:
                    position = pos
                    diff = round(degree - position, 1)
                else:
                    diff = 1
            while diff < -0.1:
                self.jog_backward(0-diff)
                time.sleep(0.3)
                pos = self.get_position()
                time.sleep(0.3)
                print(pos)
                if pos is not None:
                    position = pos
                    diff = round(degree - position, 1)
                else:
                    diff = -1

    def close(self):
        self.mount.close()
        print("Bye")

## Testing code

import matplotlib.pyplot as plt
device = ELL14K()

power = []
for i in range(180):
    device.set_angle(i)
    #time.sleep(0.5)
    print(i)

    power.append(power_meter.read)
plt.plot(power, '.')
plt.ylabel('Power(W)')
plt.xlabel('Angle(Degrees)')
plt.title("Time Delay")
plt.show()

'''

a_std = []
plt.plot(a_std,x, '.', label='with rotation')
plt.plot(test_std,x, '.', label='not moving')
plt.xlabel('Time Delay(Seconds)')
plt.ylabel('Standard Deviation(W)')
plt.show()

b_std = []
test_std = []
x = []
'''
'''
#device.home()
#time.sleep(1)
min_max = [0, 0]
angles = [0, 0]
device.set_angle(28)
time.sleep(0.5)
min_max[1]=power_meter.read
angles[1]=device.get_position()
device.set_angle(73)
time.sleep(0.5)
min_max[0]=power_meter.read
angles[0]=device.get_position()
device.home()
time.sleep(1)
print(min_max)
print(angles)
counter = [0, 0]

for i in range(100):
    print(i)
    device.set_angle(28)
    #time.sleep(0.1)
    max_val = power_meter.read
    max_angle = device.get_position()
    print(max_val)
    if max_val<0.9*min_max[1] or max_val > 1.1*min_max[1]:
        print("Horizontal Error" + str(max_val))
        counter[-1] = counter[-1] + 1
    if max_angle<0.9*angles[1] or max_angle > 1.1*angles[1]:
        print("Horizontal Error Angle" + str(max_angle))
        #counter[-1] = counter[-1] + 1
    device.set_angle(73)
   # time.sleep()
    min_val = power_meter.read
    min_angle = device.get_position()
    print(min_val)
    if min_val<0.8*min_max[0] or min_val > 1.2*min_max[0]:
        print("Vertical Error" + str(min_val))
        counter[-2] = counter[-2] + 1
    if min_angle<0.9*angles[0] or min_angle > 1.1*angles[0]:
        print("Vertical Error Angle" + str(max_angle))
        #counter[-1] = counter[-1] + 1

'''
'''

for j in range (10):
    power_array_a = []
    power_array_b = []
    power_array_test = []
    x.append((j+5)*0.1)
    device.set_angle(29)
    for i in range(50):
        time.sleep(0.5)
        power_array_test.append(power_meter.read)

    device.home()
    for i in range(50):
        device.set_angle(74)
        time.sleep((j+5)*0.1)
        power_array_a.append(power_meter.read)
        device.set_angle(88)
        time.sleep((j+5)*0.1)
        power_array_b.append(power_meter.read)
        print(i)
    a_std.append(np.std(power_array_a))
    b_std.append(np.std(power_array_b))
    test_std.append(np.std(power_array_test))
plt.plot(x, a_std, '.', label='with rotation')
plt.plot(x, test_std, '.', label='not moving')
plt.xlabel('Time Delay(Seconds)')
plt.ylabel('Standard Deviation(W)')
plt.show()
'''
​
