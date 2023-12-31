import pybullet as p
from pyrosim.neuralNetwork import NEURAL_NETWORK
import pyrosim.pyrosim as pyrosim

from motor import MOTOR
from sensor import SENSOR


class ROBOT:
    def __init__(self):
        # Load predefined robot body file
        self.id = p.loadURDF("body.urdf")
        # Load our predefined neural network
        self.nn = NEURAL_NETWORK("brain.nndf")
    
    # Create sensors for each link in the robot's body
    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)
    
    # t = time step value
    def Sense(self, t):
        for sensor in self.sensors.values():
            sensor.Get_Value(t)
    
    # Create motors for each joint in the robot's body
    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)
    
    # Activate motors
    def Act(self, t):
        for motor in self.motors.values():
            motor.Set_Value(self.id, t)
    
    # Calculate next movements
    def Think(self):
        self.nn.Update()
        self.nn.Print()