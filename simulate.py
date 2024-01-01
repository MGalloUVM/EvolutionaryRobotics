import sys

from simulation import SIMULATION


# Command line argument for headless mode...
directOrGUI = sys.argv[1].upper()
# Validate argument
if directOrGUI not in ['DIRECT','GUI']:
    print(f"Invalid argument supplied: {directOrGUI}. (Valid arguments: DIRECT, GUI)")
# CL Argument for solution ID
solutionID = int(sys.argv[2])
# Create Simulation
simulation = SIMULATION(directOrGUI, solutionID)
# Run Simulation
simulation.Run()
# Write Simulation Fitness to file
simulation.Get_Fitness()