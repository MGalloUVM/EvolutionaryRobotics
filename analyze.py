import matplotlib.pyplot as plt
import numpy as np


###
# Motor Data
###

backLegTargetAngles = np.load('data/BackLegTargetAngles.npy')
frontLegTargetAngles = np.load('data/FrontLegTargetAngles.npy')

plt.plot(backLegTargetAngles, label="Back Leg")
plt.plot(frontLegTargetAngles, label="Front Leg", color="red", alpha=0.6)
plt.title("Motor Commands")
plt.legend()
plt.show()

###
# Sensor Data
###

backLegSensorValues = np.load('data/BackLegTouch.npy')
frontLegSensorValues = np.load('data/FrontLegTouch.npy')

plt.plot(frontLegSensorValues, label="Front Leg Sensor")
plt.plot(backLegSensorValues, label="Back Leg Sensor", color="red", alpha=0.6, linewidth=1)
plt.legend()
plt.show()