import numpy as np
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import random
import time


###
# Constants
###

GRAVITY = -9.8
PI = np.pi


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
p.setGravity(0, 0, GRAVITY)

# Load predefined floor plane from pybullet_data
planeId = p.loadURDF("plane.urdf")

# Load predefined world file
p.loadSDF("world.sdf")
# Load predefined robot body file
robotId = p.loadURDF("body.urdf")
# Connect Pyroism to robot
pyrosim.Prepare_To_Simulate(robotId)

# Define our simulation length
sim_length = 1000

# Create len10000 array of zeros for future sensor data
backLegSensorValues = np.zeros(sim_length)
frontLegSensorValues = np.zeros(sim_length)

# Generate sinusoidal target angles
backLegAmplitude = PI/3
backLegFrequency = 0.05
backLegPhaseOffset = 0
backLegTargetAngles = [backLegAmplitude * np.sin(backLegFrequency * i + backLegPhaseOffset) for i in range(sim_length)]
frontLegAmplitude = PI/4
frontLegFrequency = 0.05
frontLegPhaseOffset = PI/4
frontLegTargetAngles = [frontLegAmplitude * np.sin(frontLegFrequency * i + frontLegPhaseOffset) for i in range(sim_length)]
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
        maxForce = 25
    )
    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = "Torso_FrontLeg",
        controlMode = p.POSITION_CONTROL,
        targetPosition = frontLegTargetAngles[i],
        maxForce = 25
    )
    time.sleep(1/240)

# Save sensor data to file
np.save('data/BackLegTouch.npy', backLegSensorValues)
np.save('data/FrontLegTouch.npy', frontLegSensorValues)

##
# Close physics client + GUI
##
p.disconnect()
