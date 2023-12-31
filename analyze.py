import matplotlib.pyplot as plt
import numpy as np

backLegSensorValues = np.load('data/BackLegTouch.npy')
frontLegSensorValues = np.load('data/FrontLegTouch.npy')

plt.plot(frontLegSensorValues)
plt.plot(backLegSensorValues)
plt.show()