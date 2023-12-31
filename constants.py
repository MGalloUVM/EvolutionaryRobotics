import numpy as np

PI = np.pi

###
# Simulation Variables
###

GRAVITY = -9.8
SIMULATION_LENGTH = 1000
SLEEP_PER_FRAME = 1/240
# Max force on a joint
MAX_FORCE = 25


###
# Motor Vector Generation
###

# BACK LEG
BL_AMPLITUDE = PI/3
BL_FREQUENCY = 0.05
BL_PHASE_OFFSET = 0

# FRONT LEG
FL_AMPLITUDE = PI/4
FL_FREQUENCY = 0.05
FL_PHASE_OFFSET = PI/4