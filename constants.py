import numpy as np

pi = np.pi

###
# Simulation Variables
###

simulation_length = 1000
sleep_per_frame = 1/160
numberOfGenerations = 10
populationSize = 10

###
# Physics/Body Variables
###

gravity = -9.8
# Max force on a joint
max_force = 25

numSensorNeurons = 5
numMotorNeurons = 4