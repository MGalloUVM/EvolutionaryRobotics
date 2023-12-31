import numpy as np
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import random
import time

import constants as c


###
# Physics Client Configurations
###

# Launch physics client + GUI
physicsClient = p.connect(p.GUI)
# Define an additional search path to look for files in directory
p.setAdditionalSearchPath(pybullet_data.getDataPath())
# Hide side bars in GUI
p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)

###
# World / Object Config
###

# Add force of Gravity
p.setGravity(0, 0, c.GRAVITY)

# Load predefined floor plane from pybullet_data
planeId = p.loadURDF("plane.urdf")

# Load predefined world file
p.loadSDF("world.sdf")
# Load predefined robot body file
robotId = p.loadURDF("body.urdf")
# Connect Pyroism to robot
pyrosim.Prepare_To_Simulate(robotId)

# Define our simulation length
sim_length = c.SIMULATION_LENGTH

# Initialize len10000 array of zeros for future sensor data
backLegSensorValues = np.zeros(sim_length)
frontLegSensorValues = np.zeros(sim_length)

# Generate sinusoidal target angles
backLegTargetAngles = [c.BL_AMPLITUDE * np.sin(c.BL_FREQUENCY * i + c.BL_PHASE_OFFSET) for i in range(sim_length)]
frontLegTargetAngles = [c.FL_AMPLITUDE * np.sin(c.FL_FREQUENCY * i + c.FL_PHASE_OFFSET) for i in range(sim_length)]

# Save motor data to file
np.save('data/FrontLegTargetAngles.npy', backLegTargetAngles)
np.save('data/BackLegTargetAngles.npy', frontLegTargetAngles)
# exit()

# Step through simulation
for i in range(sim_length):
    p.stepSimulation()
    # Read touch sensor values
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    # Simulate motors
    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = "Torso_BackLeg",
        controlMode = p.POSITION_CONTROL,
        targetPosition = backLegTargetAngles[i],
        maxForce = c.MAX_FORCE
    )
    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = "Torso_FrontLeg",
        controlMode = p.POSITION_CONTROL,
        targetPosition = frontLegTargetAngles[i],
        maxForce = c.MAX_FORCE
    )
    time.sleep(c.SLEEP_PER_FRAME)

# Save sensor data to file
np.save('data/BackLegTouch.npy', backLegSensorValues)
np.save('data/FrontLegTouch.npy', frontLegSensorValues)

##
# Close physics client + GUI
##
p.disconnect()
