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

SampleInterval=10 #wait time between two acceleration samples
SampleTime = 8*60*1E9   #total time to gather information 8 minutes

def formula(x,a,R,t0,t1):
    
    return a+x**2/R*np.sin(x/R*(t1-t0)*1E9) #this is what you have to solve
                                            # acceleration is second derivative of sine function
                                            # y = R sin (omega*t) with omega = v * R

def sampledata(t0,SampleTime,SampleInterval):
    sense = SenseHat()
    sense.set_imu_config(False, False, True)  # accelerometer only
    accelerations=[]
    velocities = []
    while time.time_ns ()- t0 < SampleTime:
        tstart=time.time_ns()
        data = sense.get_accelerometer_raw()
        getaccel=math.sqrt((data["x"]/G)**2 + (data["y"]/G)**2 + (data["z"]/G)**2)   # use Pythagora to calculate total acceleration in m/s²accelerations=[getaccel()]
        accelerations.append(getaccel)
        time.sleep(SampleInterval)
        velocities.append(fsolve(formula,V_0, args=(getaccel,R,tstart,time.time_ns()))[0])
        #print(accelerations)
    #return accelerations
    return velocities



t0=time.time_ns()
#verander onderstaande code zodat je een minuut lang meet, of 8 minuten
accelerations = sampledata(t0,SampleTime,SampleInterval)
#accelerations = removeoutliers(accelerations)
accel = np.median(accelerations)
t1=time.time_ns()
x=V_0
#v=fsolve(formula,V_0, args=(accel,R,t0,t1))[0]
v=accel

with open('result.txt', 'w') as f:
    f.write("{:.4f}".format(v/1000))
f.close()
