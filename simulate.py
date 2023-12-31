from simulation import SIMULATION


simulation = SIMULATION()
simulation.Run()

# # Generate sinusoidal target angles
# backLegTargetAngles = [c.bl_amplitude * np.sin(c.bl_frequency * i + c.bl_phase_offset) for i in range(sim_length)]
# frontLegTargetAngles = [c.fl_amplitude * np.sin(c.fl_frequency * i + c.fl_phase_offset) for i in range(sim_length)]

# # Save motor data to file
# np.save('data/FrontLegTargetAngles.npy', backLegTargetAngles)
# np.save('data/BackLegTargetAngles.npy', frontLegTargetAngles)