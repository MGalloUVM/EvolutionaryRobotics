import matplotlib.pyplot as plt
import numpy as np


###
# Motor Data
###

targetAngles = np.load('data/TargetAngles.npy')

plt.plot(targetAngles)
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