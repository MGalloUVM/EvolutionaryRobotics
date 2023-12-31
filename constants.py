import numpy as np

pi = np.pi

###
# Simulation Variables
###

gravity = -9.8
simulation_length = 1000
sleep_per_frame = 1/240
# Max force on a joint
max_force = 25


###
# Motor Vector Generation
###

# BACK LEG
bl_amplitude = pi/3
bl_frequency = 0.05
bl_phase_offset = 0

# FRONT LEG
fl_amplitude = pi/4
fl_frequency = 0.05
fl_phase_offset = pi/4