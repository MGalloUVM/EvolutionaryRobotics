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

    def Run(self):
        # Step through simulation
        for i in range(c.simulation_length):
            p.stepSimulation()
            # # Read touch sensor values
            # backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
            # frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
            # # Simulate motors
            # pyrosim.Set_Motor_For_Joint(
            #     bodyIndex = robotId,
            #     jointName = "Torso_BackLeg",
            #     controlMode = p.POSITION_CONTROL,
            #     targetPosition = backLegTargetAngles[i],
            #     maxForce = c.max_force
            # )
            # pyrosim.Set_Motor_For_Joint(
            #     bodyIndex = robotId,
            #     jointName = "Torso_FrontLeg",
            #     controlMode = p.POSITION_CONTROL,
            #     targetPosition = frontLegTargetAngles[i],
            #     maxForce = c.max_force
            # )
            sleep(c.sleep_per_frame)
    
    def __del__(self):
        p.disconnect()