import numpy as np
import os
import pyrosim.pyrosim as pyrosim
import random
from time import sleep

import constants as c


class SOLUTION:
    def __init__(self, myID):
        self.myID = myID
        self.weights = np.random.rand(c.numSensorNeurons, c.numMotorNeurons) * 2 - 1
    
    def Set_ID(self, newID):
        self.myID = newID
    
    # Generate robot's world, body, neural network
    #   Start Simulation
    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system(f"python3 simulate.py {directOrGUI} {self.myID} &>log.txt &")

    # Waits for simulation to end, reads in fitness files
    def Wait_For_Simulation_To_End(self):
        while not os.path.exists(f"fitness{self.myID}.txt"):
            sleep(0.01)
        with open(f"fitness{self.myID}.txt", 'r') as fitnessFile:
            self.fitness = float(fitnessFile.readline().strip())
        # Remove fitness file after read
        os.system(f"rm fitness{self.myID}.txt")
    
    def Mutate(self):
        # Choose a random row to mutate
        randomRow = random.randint(0, self.weights.shape[0] - 1)
        randomCol = random.randint(0, self.weights.shape[1] - 1)
        self.weights[randomRow, randomCol] = random.random() * 2 - 1

    # Create our world
    def Create_World(self):
        # Only execute if file isn't already built
        if os.path.exists("world.sdf"):
            return
        # Set output file's name
        pyrosim.Start_SDF("world.sdf")
        # Define cube dimensions (L, W, H)
        cube_dim = (1, 1, 1)
        # Define cube positions (X, Y, Z)
        cube_pos = (-5, 5, cube_dim[2]/2)
        # Write to output
        pyrosim.Send_Cube(
            name="Obstacle",
            pos=[cube_pos[0], cube_pos[1], cube_pos[2]],
            size=[cube_dim[0], cube_dim[1], cube_dim[2]])
        # Close file
        pyrosim.End()


    # Generate Robot Body
    def Create_Body(self):
        if os.path.exists("body.urdf"):
            return
        # Define output file for URDF writing
        pyrosim.Start_URDF("body.urdf")

        # Absolute
        pyrosim.Send_Cube(
            name="Torso",
            pos=[0, 0, 1],
            size=[1, 1, 1])
        pyrosim.Send_Cube(
            name="FrontLeg",
            pos=[0, 0.5, 0],
            size=[0.2, 1, 0.2])
        pyrosim.Send_Cube(
            name="BackLeg",
            pos=[0, -0.5, 0],
            size=[0.2, 1, 0.2])
        pyrosim.Send_Cube(
            name="LeftLeg",
            pos=[-0.5, 0, 0],
            size=[1, 0.2, 0.2])
        pyrosim.Send_Cube(
            name="RightLeg",
            pos=[0.5, 0, 0],
            size=[1, 0.2, 0.2])
        
        # Relative
        pyrosim.Send_Cube(
            name="FrontLowerLeg",
            pos=[0, 0, -0.5],
            size=[0.2, 0.2, 1])
        pyrosim.Send_Cube(
            name="BackLowerLeg",
            pos=[0, 0, -0.5],
            size=[0.2, 0.2, 1])
        pyrosim.Send_Cube(
            name="LeftLowerLeg",
            pos=[0, 0, -0.5],
            size=[0.2, 0.2, 1])
        pyrosim.Send_Cube(
            name="RightLowerLeg",
            pos=[0, 0, -0.5],
            size=[0.2, 0.2, 1])        

        # Define our Joints
        pyrosim.Send_Joint(
            name = "Torso_FrontLeg",
            parent = "Torso", child = "FrontLeg",
            type = "revolute",
            position = [0, 0.5, 1],
            jointAxis="1 0 0")
        pyrosim.Send_Joint(
            name = "Torso_BackLeg",
            parent = "Torso", child = "BackLeg",
            type = "revolute",
            position = [0, -0.5, 1],
            jointAxis="1 0 0")
        pyrosim.Send_Joint(
            name = "Torso_LeftLeg",
            parent = "Torso", child = "LeftLeg",
            type = "revolute",
            position = [-0.5, 0, 1],
            jointAxis="0 1 0")
        pyrosim.Send_Joint(
            name = "Torso_RightLeg",
            parent = "Torso", child = "RightLeg",
            type = "revolute",
            position = [0.5, 0, 1],
            jointAxis="0 1 0")
        pyrosim.Send_Joint(
            name = "FrontLeg_FrontLowerLeg",
            parent = "FrontLeg", child = "FrontLowerLeg",
            type = "revolute",
            position = [0, 1, 0],
            jointAxis="1 0 0")
        pyrosim.Send_Joint(
            name = "BackLeg_BackLowerLeg",
            parent = "BackLeg", child = "BackLowerLeg",
            type = "revolute",
            position = [0, -1, 0],
            jointAxis="1 0 0")
        pyrosim.Send_Joint(
            name = "LeftLeg_LeftLowerLeg",
            parent = "LeftLeg", child = "LeftLowerLeg",
            type = "revolute",
            position = [-1, 0, 0],
            jointAxis="0 1 0")
        pyrosim.Send_Joint(
            name = "RightLeg_RightLowerLeg",
            parent = "RightLeg", child = "RightLowerLeg",
            type = "revolute",
            position = [1, 0, 0],
            jointAxis="0 1 0")

        # Close file
        pyrosim.End()
    
    # Generate Robot Brain
    def Create_Brain(self):
        # Define output file for URDF writing
        pyrosim.Start_URDF(f"brain{self.myID}.nndf")
        # Create a sensor neuron on our links
        pyrosim.Send_Sensor_Neuron(name=0 , linkName="FrontLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=1 , linkName="BackLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=2 , linkName="LeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=3 , linkName="RightLowerLeg")
        # Create a motor neuron for all our joints
        pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=5, jointName="Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron(name=6, jointName="Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron(name=7, jointName="Torso_RightLeg")
        pyrosim.Send_Motor_Neuron(name=8, jointName="FrontLeg_FrontLowerLeg")
        pyrosim.Send_Motor_Neuron(name=9, jointName="BackLeg_BackLowerLeg")
        pyrosim.Send_Motor_Neuron(name=10, jointName="LeftLeg_LeftLowerLeg")
        pyrosim.Send_Motor_Neuron(name=11, jointName="RightLeg_RightLowerLeg")
        # Generate Synapses
        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                # Target Neuron starts numRows + currentColumn
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn+c.numSensorNeurons, weight=self.weights[currentRow][currentColumn])
        # Close file
        pyrosim.End()