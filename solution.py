import numpy as np
import os
import pyrosim.pyrosim as pyrosim


class SOLUTION:
    def __init__(self):
        self.weights = np.random.rand(3, 2) * 2 - 1
    
    # Generate robot's world, body, neural network
    def Evaluate(self):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system('python3 simulate.py')

    # Create our world
    def Create_World(self):
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
        # Define output file for URDF writing
        pyrosim.Start_URDF("body.urdf")
        # Define dimensions (L, W, H)
        dim = (1, 1, 1)
        # Define positions (X, Y, Z) ABSOLUTE
        pos = (0, 0, 1.5)
        # Write to output
        pyrosim.Send_Cube(
            name="Torso",
            pos=[pos[0], pos[1], pos[2]],
            size=[dim[0], dim[1], dim[2]])
        # Define dimensions (L, W, H)
        dim = (1, 1, 1)
        # Define positions (X, Y, Z) RELATIVE
        pos = (0.5, 0, -0.5)
        # Write to output
        pyrosim.Send_Cube(
            name="FrontLeg",
            pos=[pos[0], pos[1], pos[2]],
            size=[dim[0], dim[1], dim[2]])
        
        # Define dimensions (L, W, H)
        dim = (1, 1, 1)
        # Define positions (X, Y, Z) RELATIVE
        pos = (-0.5, 0, -0.5)
        # Write to output
        pyrosim.Send_Cube(
            name="BackLeg",
            pos=[pos[0], pos[1], pos[2]],
            size=[dim[0], dim[1], dim[2]])

        # Define our Joints
        pyrosim.Send_Joint(
            name = "Torso_FrontLeg",
            parent = "Torso", child = "FrontLeg",
            type = "revolute",
            position = [0.5, 0, 1])
        pyrosim.Send_Joint(
            name = "Torso_BackLeg",
            parent = "Torso", child = "BackLeg",
            type = "revolute",
            position = [-0.5, 0, 1])

        # Close file
        pyrosim.End()
    
    # Generate Robot Brain
    def Create_Brain(self):
        # Define output file for URDF writing
        pyrosim.Start_URDF("brain.nndf")
        # Create a sensor neuron on our links
        pyrosim.Send_Sensor_Neuron(name=0 , linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1 , linkName="BackLeg")
        pyrosim.Send_Sensor_Neuron(name=2 , linkName="FrontLeg")
        # Create a motor neuron for all our joints
        pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")
        # Generate Synapses
        for currentRow in [0, 1, 2]:
            for currentColumn in [0, 1]:
                # Target Neuron starts at 3, so add 3 to currentColumn
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn+3, weight=self.weights[currentRow][currentColumn])
        # Close file
        pyrosim.End()