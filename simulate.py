import pybullet as p
import time

# Launch physics client GUI
physicsClient = p.connect(p.GUI)
# Hide side bars in GUI
p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)

# Load predefined object from file
p.loadSDF("box.sdf")

for x in range(1000):
    p.stepSimulation()
    print(x)
    time.sleep(1/60)

# Close physics client GUI
p.disconnect()
