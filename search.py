import os
from glob import glob

from parallelHillClimber import PARALLEL_HILL_CLIMBER


def Clean_Up_Files():
    # Remove any lingering files using wildcards with glob
    file_patterns = ["body.urdf", "world.sdf", "brain*.nndf", "fitness*.txt"]
    for pattern in file_patterns:
        for file in glob(pattern):
            os.system(f"rm {file}")

def Main():
    Clean_Up_Files()

    phc = PARALLEL_HILL_CLIMBER()
    phc.Evolve()
    phc.Show_Best()

if __name__=="__main__":
    Main()