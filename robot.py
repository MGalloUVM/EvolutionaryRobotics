import os
import numpy as np
import pybullet as p
from pyrosim.neuralNetwork import NEURAL_NETWORK
import pyrosim.pyrosim as pyrosim

import constants as c
from motor import MOTOR
from sensor import SENSOR


class ROBOT:
    def __init__(self, solutionID):
        self.solutionID = solutionID
        # Load predefined robot body file
        self.robotId = p.loadURDF("body.urdf")
        # Load our predefined neural network
        self.nn = NEURAL_NETWORK(f"brain{self.solutionID}.nndf")
        os.system(f"rm brain{self.solutionID}.nndf")

        # Record position of head link throughout simulation
        #    for later fitness evaluations
        self.hipsLinkPositions = np.zeros(c.simulation_length)
        self.leftFootLinkPositions = np.zeros(c.simulation_length)
        self.rightFootLinkPositions = np.zeros(c.simulation_length)
    
    # Create sensors for each link in the robot's body
    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)
    
    # t = time step value
    def Sense(self, t):
        """
        $ Link Name: Head, Link ID: 0
        $ Link Name: Hips, Link ID: 1
        $ Link Name: LeftUpperLeg, Link ID: 2
        $ Link Name: LeftLowerLeg, Link ID: 3
        $ Link Name: LeftFoot, Link ID: 4
        $ Link Name: RightUpperLeg, Link ID: 5
        $ Link Name: RightLowerLeg, Link ID: 6
        $ Link Name: RightFoot, Link ID: 7
        $ Link Name: LeftUpperArm, Link ID: 8
        $ Link Name: LeftLowerArm, Link ID: 9
        """
        # Record link positions
        hipsPosition = p.getLinkState(self.robotId, 1)[0]
        self.hipsLinkPositions[t] = hipsPosition[0]
        leftFootPosition = p.getLinkState(self.robotId, 4)[0]
        self.leftFootLinkPositions[t] = leftFootPosition[0]
        rightFootPosition = p.getLinkState(self.robotId, 7)[0]
        self.rightFootLinkPositions[t] = rightFootPosition[0]
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
                desiredAngle = c.motorJointRange * self.nn.Get_Value_Of(neuronName)
                self.motors[jointName].Set_Value(self.robotId, desiredAngle)
    
    # Calculate next movements
    def Think(self):
        self.nn.Update()
    
    def Get_Fitness(self):
        # Head height
        MIN_HEAD_HEIGHT = 1.8
        HEAD_HEIGHT_PENALTY_FACTOR = -5.0
        # Forward movement
        FORWARD_MOVEMENT_REWARD_FACTOR = 6.0
        # Upright posture, reduce rotation
        # Define thresholds for how much roll and pitch are acceptable
        MAX_ROLL_PITCH = np.pi / 14
        UPRIGHT_POSTURE_PENALTY_FACTOR = -10
        # Alternative stepping...
        ALTERNATIVE_STEP_THRESHOLD = 0.5
        SEQUENTIAL_MOVEMENT_REWARD_FACTOR = 1.0

        def penalize_for_low_head_height(headZ):
            # Gradual penalty based on the distance from the minimum height
            penalty = max(0, MIN_HEAD_HEIGHT - headZ) * HEAD_HEIGHT_PENALTY_FACTOR
            return penalty

        def reward_for_forward_movement():
            # Consider the forward displacement of the robot's body (e.g., torso)
            initial_position = self.hipsLinkPositions[0]
            final_position = self.hipsLinkPositions[-1]
            forward_displacement = final_position - initial_position
            return forward_displacement * FORWARD_MOVEMENT_REWARD_FACTOR

        def reward_for_upright_posture():
            # Get the orientation of the torso or head in quaternion
            _, orientation_quat = p.getBasePositionAndOrientation(self.robotId)

            # Convert quaternion to Euler angles (roll, pitch, yaw)
            roll, pitch, _ = p.getEulerFromQuaternion(orientation_quat)

            # Calculate the deviation from being perfectly upright (0 roll and pitch)
            roll_deviation = max(0, abs(roll) - MAX_ROLL_PITCH)
            pitch_deviation = max(0, abs(pitch) - MAX_ROLL_PITCH)

            # Penalize based on the deviation, more deviation leads to more penalty
            penalty = (roll_deviation + pitch_deviation) * UPRIGHT_POSTURE_PENALTY_FACTOR

            # Convert penalty to a positive reward value
            return max(0, 10 + penalty)  # Ensure reward is not negative
        
        def reward_for_foot_movement():
            mean_left_foot_movement = mean_positive_movement(self.leftFootLinkPositions)
            mean_right_foot_movement = mean_positive_movement(self.rightFootLinkPositions)

            return (mean_left_foot_movement + mean_right_foot_movement) / 2

        def mean_positive_movement(linkPositions):
            differences = np.diff(linkPositions)
            positive_differences = np.clip(differences, 0, None)
            return np.mean(positive_differences)

        def alternative_stepping_factor():
            rightFootSensorValues = self.sensors['RightFoot'].values
            leftFootSensorValues = self.sensors['LeftFoot'].values
            feetSensorDiff = np.abs(rightFootSensorValues - leftFootSensorValues)

            return np.count_nonzero(feetSensorDiff > ALTERNATIVE_STEP_THRESHOLD) / len(feetSensorDiff)
        
        def reward_sequential_foot_movements():
            # Calculate the differences in position for each foot over time
            left_foot_differences = np.diff(self.leftFootLinkPositions)
            right_foot_differences = np.diff(self.rightFootLinkPositions)

            # Identify steps: positive differences indicate a forward movement
            left_steps = left_foot_differences > 0
            right_steps = right_foot_differences > 0

            # Count the number of times the feet move in an alternating fashion
            # This is a simplistic way to encourage alternating steps
            alternating_steps = 0
            for i in range(1, len(left_steps)):  # start from 1 because we compare with the previous step
                # If one foot moves forward and the other does not, increment the count
                if (left_steps[i] and not right_steps[i-1]) or (right_steps[i] and not left_steps[i-1]):
                    alternating_steps += 1

            # Normalize the reward by the number of steps taken
            # to prevent the reward from merely increasing with simulation time
            total_steps = np.count_nonzero(left_steps) + np.count_nonzero(right_steps)
            if total_steps > 0:
                reward = (alternating_steps / total_steps) * SEQUENTIAL_MOVEMENT_REWARD_FACTOR
            else:
                reward = 0

            return reward

        # Calculate fitness components
        head_position = p.getLinkState(self.robotId, 0)[0]
        head_height_penalty = penalize_for_low_head_height(head_position[2])
        forward_movement_reward = reward_for_forward_movement()
        upright_posture_reward = reward_for_upright_posture()
        foot_movement_reward = reward_for_foot_movement()
        stepping_factor = alternative_stepping_factor()
        sequential_foot_movement_reward = reward_sequential_foot_movements()

        # Combine fitness components
        fitness = (forward_movement_reward +
                   foot_movement_reward +
                   upright_posture_reward +
                   head_height_penalty +
                   sequential_foot_movement_reward) * stepping_factor

        # Save the fitness value to a file
        with open(f"tmp{self.solutionID}.txt", 'w') as outfile:
            outfile.write(str(fitness))
        os.system(f"mv tmp{self.solutionID}.txt fitness{self.solutionID}.txt")
        
        return fitness