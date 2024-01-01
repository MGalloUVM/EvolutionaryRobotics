import numpy as np

pi = np.pi

###
# Simulation Variables
###

simulation_length = 1500
sleep_per_frame = 1/160
numberOfGenerations = 18
populationSize = 18

###
# Physics/Body Variables
###

gravity = -9.8
motorJointRange = 0.6
# Max force on a joint
max_force = 25

numSensorNeurons = 4
numMotorNeurons = 8