import pybullet as p
from pyrosim.neuralNetwork import NEURAL_NETWORK
import pyrosim.pyrosim as pyrosim

from motor import MOTOR
from sensor import SENSOR


class ROBOT:
    def __init__(self):
        # Load predefined robot body file
        self.robotId = p.loadURDF("body.urdf")
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
    def Act(self):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                self.motors[jointName].Set_Value(self.robotId, desiredAngle)
                print(neuronName, jointName, desiredAngle)
    
    # Calculate next movements
    def Think(self):
        self.nn.Update()