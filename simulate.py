import pybullet as p
import pybullet_data
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


# Step through simulation
for x in range(1000):
    p.stepSimulation()
    print(x)
    time.sleep(1/60)

##
# Close physics client + GUI
##
p.disconnect()
