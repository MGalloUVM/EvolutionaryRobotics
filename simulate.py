import sys

from simulation import SIMULATION


# Command line argument for headless mode...
directOrGUI = sys.argv[1].upper()
# Validate argument
if directOrGUI not in ['DIRECT','GUI']:
    print(f"Invalid argument supplied: {directOrGUI}. (Valid arguments: DIRECT, GUI)")
simulation = SIMULATION(directOrGUI)
simulation.Run()
simulation.Get_Fitness()