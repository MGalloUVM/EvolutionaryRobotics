import pybullet as p
import time

# Launch physics client GUI
physicsClient = p.connect(p.GUI)

for x in range(1000):
    p.stepSimulation()
    print(x)
    time.sleep(1/60)

# Close physics client GUI
p.disconnect()
