import numpy as np
import pybullet as p
import pyrosim.pyrosim as pyrosim

import constants as c


class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        self.Prepare_To_Act()
    
    def Prepare_To_Act(self):
        self.amplitude = c.fl_amplitude
        self.frequency = c.fl_frequency
        if self.jointName == "Torso_FrontLeg":
            self.frequency = c.fl_frequency / 2
        self.offset = c.fl_phase_offset
        # Generate sinusoidal target angles
        self.motorValues = [self.amplitude * np.sin(self.frequency * i + self.offset) for i in range(c.simulation_length)]
    
    def Set_Value(self, robot, t):
        pyrosim.Set_Motor_For_Joint(
            bodyIndex = robot,
            jointName = self.jointName,
            controlMode = p.POSITION_CONTROL,
            targetPosition = self.motorValues[t],
            maxForce = c.max_force)

    def Save_Values(self):
        # Save motor data to file
        np.save(f"data/{self.jointName}MotorValues.npy", self.motorValues)