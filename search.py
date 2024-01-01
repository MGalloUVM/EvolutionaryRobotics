import os

from parallelHillClimber import PARALLEL_HILL_CLIMBER

# Remove any lingering files
os.system("rm body.urdf; rm world.sdf; rm brain*.nndf; rm fitness*.txt")

phc = PARALLEL_HILL_CLIMBER()
phc.Evolve()
phc.Show_Best()

# Clean up Body and World files
os.system("rm body.urdf; rm world.sdf")