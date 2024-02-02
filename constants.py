import numpy as np

pi = np.pi

###
# Simulation Variables
###

simulation_length = 1500
sleep_per_frame = 1/160
numberOfGenerations = 10
populationSize = 500

###
# Physics/Body Variables
###

gravity = -9.8
motorJointRange = 0.8
# Max force on a joint
max_force = 35

numSensorNeurons = 12
numMotorNeurons = 12