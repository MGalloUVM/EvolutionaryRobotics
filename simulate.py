import numpy as np
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
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
        targetPosition = PI / 4.0,
        maxForce = 500
    )
    time.sleep(1/60)

# Save sensor data to file
np.save('data/BackLegTouch.npy', backLegSensorValues)
np.save('data/FrontLegTouch.npy', frontLegSensorValues)

##
# Close physics client + GUI
##
p.disconnect()
