import numpy as np

pi = np.pi

###
# Simulation Variables
###

simulation_length = 1000
sleep_per_frame = 1/160
numberOfGenerations = 1
populationSize = 1

###
# Physics/Body Variables
###

gravity = -9.8
# Max force on a joint
max_force = 25

numSensorNeurons = 3
numMotorNeurons = 2