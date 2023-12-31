import pybullet as p

from motor import MOTOR
from sensor import SENSOR


class ROBOT:
    def __init__(self):
        self.motors = {}
        self.sensors = {}
        
        # Load predefined robot body file
        self.id = p.loadURDF("body.urdf")