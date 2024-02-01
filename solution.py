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

        # Links
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1.6], size=[0.2, 0.5, 0.6])

        # Upper Body
        pyrosim.Send_Cube(name="Head", pos=[0, 0, 0.175], size=[0.35, 0.35, 0.35])
        # Arms
        pyrosim.Send_Cube(name="LeftUpperArm", pos=[0, 0, -0.2], size=[0.2, 0.2, 0.4])
        pyrosim.Send_Cube(name="RightUpperArm", pos=[0, 0, -0.2], size=[0.2, 0.2, 0.4])
        pyrosim.Send_Cube(name="LeftLowerArm", pos=[0, 0, -0.2], size=[0.2, 0.2, 0.4])
        pyrosim.Send_Cube(name="RightLowerArm", pos=[0, 0, -0.2], size=[0.2, 0.2, 0.4])
        # Lower Body
        pyrosim.Send_Cube(name="Hips", pos=[0, 0, -0.1], size=[0.2, 0.5, 0.2])
        # Legs
        pyrosim.Send_Cube(name="LeftUpperLeg", pos=[0, 0, -0.25], size=[0.2, 0.2, 0.5])
        pyrosim.Send_Cube(name="RightUpperLeg", pos=[0, 0, -0.25], size=[0.2, 0.2, 0.5])
        pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0, 0, -0.25], size=[0.2, 0.2, 0.5])
        pyrosim.Send_Cube(name="RightLowerLeg", pos=[0, 0, -0.25], size=[0.2, 0.2, 0.5])
        pyrosim.Send_Cube(name="LeftFoot", pos=[0.075, 0, -0.05], size=[0.35, 0.2, 0.1])
        pyrosim.Send_Cube(name="RightFoot", pos=[0.075, 0, -0.05], size=[0.35, 0.2, 0.1])

        # Joints

        # Root Joints
        pyrosim.Send_Joint(name="Torso_Head", parent="Torso", child="Head", type="revolute", position=[0, 0, 1.9], jointAxis="0 1 0")
        pyrosim.Send_Joint(name="Torso_Hips", parent="Torso", child="Hips", type="revolute", position=[0, 0, 1.3], jointAxis="0 1 0")
        # Arms (Still off root torso)
        pyrosim.Send_Joint(name="Torso_LeftUpperArm", parent="Torso", child="LeftUpperArm", type="revolute", position=[0, -0.35, 1.9], jointAxis="0 1 0")
        pyrosim.Send_Joint(name="Torso_RightUpperArm", parent="Torso", child="RightUpperArm", type="revolute", position=[0, 0.35, 1.9], jointAxis="0 1 0")
        pyrosim.Send_Joint(name="LeftUpperArm_LeftLowerArm", parent="LeftUpperArm", child="LeftLowerArm", type="revolute", position=[0, 0, -0.4], jointAxis="0 1 0")
        pyrosim.Send_Joint(name="RightUpperArm_RightLowerArm", parent="RightUpperArm", child="RightLowerArm", type="revolute", position=[0, 0, -0.4], jointAxis="0 1 0")
        # Legs
        pyrosim.Send_Joint(name="Hips_LeftUpperLeg", parent="Hips", child="LeftUpperLeg", type="revolute", position=[0, -0.15, -0.2], jointAxis="0 1 0")
        pyrosim.Send_Joint(name="Hips_RightUpperLeg", parent="Hips", child="RightUpperLeg", type="revolute", position=[0, 0.15, -0.2], jointAxis="0 1 0")
        pyrosim.Send_Joint(name="LeftUpperLeg_LeftLowerLeg", parent="LeftUpperLeg", child="LeftLowerLeg", type="revolute", position=[0, 0, -0.5], jointAxis="0 1 0")
        pyrosim.Send_Joint(name="RightUpperLeg_RightLowerLeg", parent="RightUpperLeg", child="RightLowerLeg", type="revolute", position=[0, 0, -0.5], jointAxis="0 1 0")
        pyrosim.Send_Joint(name="LeftLowerLeg_LeftFoot", parent="LeftLowerLeg", child="LeftFoot", type="revolute", position=[0, 0, -0.5], jointAxis="0 1 0")
        pyrosim.Send_Joint(name="RightLowerLeg_RightFoot", parent="RightLowerLeg", child="RightFoot", type="revolute", position=[0, 0, -0.5], jointAxis="0 1 0")

        # Close file;
        pyrosim.End()
    
    # Generate Robot Brain
    def Create_Brain(self):
        # Define output file for URDF writing
        pyrosim.Start_URDF(f"brain{self.myID}.nndf")
        # Create a sensor neuron on our links
        pyrosim.Send_Sensor_Neuron(name=0, linkName="Head")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="LeftUpperArm")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="RightUpperArm")
        pyrosim.Send_Sensor_Neuron(name=3, linkName="LeftLowerArm")
        pyrosim.Send_Sensor_Neuron(name=4, linkName="RightLowerArm")
        pyrosim.Send_Sensor_Neuron(name=5, linkName="Hips")
        pyrosim.Send_Sensor_Neuron(name=6, linkName="LeftUpperLeg")
        pyrosim.Send_Sensor_Neuron(name=7, linkName="RightUpperLeg")
        pyrosim.Send_Sensor_Neuron(name=8, linkName="LeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=9, linkName="RightLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=10, linkName="LeftFoot")
        pyrosim.Send_Sensor_Neuron(name=11, linkName="RightFoot")
        # Create a motor neuron for all our joints
        pyrosim.Send_Motor_Neuron(name=12, jointName="Torso_Head")
        pyrosim.Send_Motor_Neuron(name=13, jointName="Torso_Hips")
        pyrosim.Send_Motor_Neuron(name=14, jointName="Torso_LeftUpperArm")
        pyrosim.Send_Motor_Neuron(name=15, jointName="Torso_RightUpperArm")
        pyrosim.Send_Motor_Neuron(name=16, jointName="LeftUpperArm_LeftLowerArm")
        pyrosim.Send_Motor_Neuron(name=17, jointName="RightUpperArm_RightLowerArm")
        pyrosim.Send_Motor_Neuron(name=18, jointName="Hips_LeftUpperLeg")
        pyrosim.Send_Motor_Neuron(name=19, jointName="Hips_RightUpperLeg")
        pyrosim.Send_Motor_Neuron(name=20, jointName="LeftUpperLeg_LeftLowerLeg")
        pyrosim.Send_Motor_Neuron(name=21, jointName="RightUpperLeg_RightLowerLeg")
        pyrosim.Send_Motor_Neuron(name=22, jointName="LeftLowerLeg_LeftFoot")
        pyrosim.Send_Motor_Neuron(name=23, jointName="RightLowerLeg_RightFoot")
        # Generate Synapses
        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                # Target Neuron starts numRows + currentColumn
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn+c.numSensorNeurons, weight=self.weights[currentRow][currentColumn])
        # Close file
        pyrosim.End()