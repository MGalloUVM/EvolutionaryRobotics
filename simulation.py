import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
from time import sleep

import constants as c
from robot import ROBOT
from world import WORLD


class SIMULATION:
    def __init__(self, directOrGUI, solutionID):
        self.directOrGUI = directOrGUI
        # Launch physics client
        if self.directOrGUI == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)
        # Define an additional search path to look for files in directory
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        # Hide side bars in GUI
        p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
        # Add force of Gravity
        p.setGravity(0, 0, c.gravity)

        self.world = WORLD()
        self.robot = ROBOT(solutionID)

        # Connect Pyroism to robot
        pyrosim.Prepare_To_Simulate(self.robot.robotId)
        # # Prepare robot for sensing
        self.robot.Prepare_To_Sense()
        # Create/link robot motors for acting
        self.robot.Prepare_To_Act()

    def Run(self):
        # Step through simulation
        #   t: time step
        for t in range(c.simulation_length):
            p.stepSimulation()
            # Read sensor values (For saving sensor values throughout run)
            self.robot.Sense(t)
            # Use our neural net to figure out what to do next
            self.robot.Think()
            # Apply motor values
            self.robot.Act()
            # If visually simulating, sleep between frames
            if self.directOrGUI == "GUI":
                sleep(c.sleep_per_frame)
    
    def Get_Fitness(self):
        self.robot.Get_Fitness()
    
    def __del__(self):
        p.disconnect()