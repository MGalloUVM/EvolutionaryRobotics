import os

from parallelHillClimber import PARALLEL_HILL_CLIMBER

# Remove any lingering files
for file in ["body.urdf", "world.sdf", "brain*.nndf", "fitness*.txt"]:
    if os.path.exists(file):
        os.system(f"rm {file}")

phc = PARALLEL_HILL_CLIMBER()
phc.Evolve()
phc.Show_Best()