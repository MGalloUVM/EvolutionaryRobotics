import pybullet as p


class WORLD:
    def __init__(self):
        # Load predefined floor plane from pybullet_data
        self.planeId = p.loadURDF("plane.urdf")
        # Load predefined world file
        p.loadSDF("world.sdf")