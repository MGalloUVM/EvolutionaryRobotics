import os

from parallelHillClimber import PARALLEL_HILL_CLIMBER


phc = PARALLEL_HILL_CLIMBER()
phc.Evolve()
phc.Show_Best()

# Remove Body and World Files
os.system("rm body.urdf; rm world.sdf")