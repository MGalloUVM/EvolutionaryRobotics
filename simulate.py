from simulation import SIMULATION


simulation = SIMULATION()
simulation.Run()

# # Initialize len10000 array of zeros for future sensor data
# backLegSensorValues = np.zeros(sim_length)
# frontLegSensorValues = np.zeros(sim_length)

# # Generate sinusoidal target angles
# backLegTargetAngles = [c.bl_amplitude * np.sin(c.bl_frequency * i + c.bl_phase_offset) for i in range(sim_length)]
# frontLegTargetAngles = [c.fl_amplitude * np.sin(c.fl_frequency * i + c.fl_phase_offset) for i in range(sim_length)]

# # Save motor data to file
# np.save('data/FrontLegTargetAngles.npy', backLegTargetAngles)
# np.save('data/BackLegTargetAngles.npy', frontLegTargetAngles)
# # exit()

# # Save sensor data to file
# np.save('data/BackLegTouch.npy', backLegSensorValues)
# np.save('data/FrontLegTouch.npy', frontLegSensorValues)