import numpy as np

pi = np.pi

###
# Simulation Variables
###

simulation_length = 1500
sleep_per_frame = 1/160
numberOfGenerations = 100
populationSize = 10

###
# Physics/Body Variables
###

gravity = -9.8
motorJointRange = 0.7
# Max force on a joint
max_force = 30

numSensorNeurons = 12
numMotorNeurons = 12