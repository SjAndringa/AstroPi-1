import math
import time
#import RTIMU
from sense_hat import SenseHat
import numpy as np
from scipy.optimize import fsolve

R = 6.7885E6 # radius earth + height ESA
OMEGA_0 = 0.00116 # initial estimate of angle velocity

V_0 = OMEGA_0*R #initial estimate of velocity, in m/s

G=9.80665 #Gforce, used to recalculate accelerometer from Gs to m/s²
            # maybe G isn't that value at that height

def initialize():
    sense = SenseHat()
    sense.set_imu_config(False, False, True)  # accelerometer only


def getaccel():
    sense = SenseHat()
    data = sense.get_accelerometer_raw()
    return math.sqrt((data["x"]/G)**2 + (data["y"]/G)**2 + (data["z"]/G)**2)   # use Pythagora to calculate total acceleration in m/s²
    #return 25

def formula(x,a,R,t0,t1):
    
    return a+x**2/R*np.sin(x/R*(t1-t0)*1E9) #this is what you have to solve
                                            # acceleration is second derivative of sine function
                                            # y = R sin (omega*t) with omega = v * R


initialize
t0=time.time_ns()
accel = getaccel()
t1=time.time_ns()
x=V_0
v=fsolve(formula,V_0, args=(accel,R,t0,t1))

f = open('result.txt', 'w')
print(round(v[0]/1000,4),file=f)
f.close()