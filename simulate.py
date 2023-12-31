import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import time


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
p.setGravity(0, 0, -9.8)

# Load predefined floor plane from pybullet_data
planeId = p.loadURDF("plane.urdf")

# Load predefined world file
p.loadSDF("world.sdf")
# Load predefined robot body file
robotId = p.loadURDF("body.urdf")
# Connect Pyroism to robot
pyrosim.Prepare_To_Simulate(robotId)

# Step through simulation
for _ in range(1000):
    p.stepSimulation()
    # Read touch sensor value on BackLeg
    backLegTouch = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    print(backLegTouch)
    time.sleep(1/60)

##
# Close physics client + GUI
##
p.disconnect()
