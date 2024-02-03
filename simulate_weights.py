import os
from glob import glob
import sys
from numpy import load

from solution import SOLUTION


def Clean_Up_Files():
    # Remove any lingering files using wildcards with glob
    file_patterns = ["body.urdf", "world.sdf", "brain*.nndf", "fitness*.txt"]
    for pattern in file_patterns:
        for file in glob(pattern):
            os.system(f"rm {file}")

def Main():
    Clean_Up_Files()
    # CL Argument for weights file name
    weightsFileName = sys.argv[1]
    # Create new solution
    solution = SOLUTION(0)
    # Load our custom weights
    weights = load(weightsFileName)
    solution.weights = weights
    # Run Simulation
    solution.Start_Simulation("GUI")

if __name__=="__main__":
    Main()