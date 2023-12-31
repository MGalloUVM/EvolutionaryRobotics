import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
from time import sleep

import constants as c
from robot import ROBOT
from world import WORLD


class SIMULATION:
    def __init__(self):
        # Launch physics client + GUI
        self.physicsClient = p.connect(p.GUI)
        # Define an additional search path to look for files in directory
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        # Hide side bars in GUI
        p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
        # Add force of Gravity
        p.setGravity(0, 0, c.gravity)

        self.world = WORLD()
        self.robot = ROBOT()

        # Connect Pyroism to robot
        pyrosim.Prepare_To_Simulate(self.robot.id)
        # Prepare robot for sensing
        self.robot.Prepare_To_Sense()
        # Prepare robot motor values for acting
        self.robot.Prepare_To_Act()

    def Run(self):
        # Step through simulation
        #   t: time step
        for t in range(c.simulation_length):
            p.stepSimulation()
            # Read sensor values
            self.robot.Sense(t)
            # Apply motor values
            self.robot.Act(t)
            sleep(c.sleep_per_frame)
    
    def __del__(self):
        p.disconnect()