import numpy as np
import pyrosim.pyrosim as pyrosim

import constants as c


class SENSOR:
    def __init__(self, linkName):
        # Array of zeros for future sensor data
        self.values = np.zeros(c.simulation_length)
        self.linkName = linkName
    
    # t = time step value
    def Get_Value(self, t):
        self.values[t] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
    
    # Write sensor data to a file
    def Save_Values(self):
        np.save(f"data/{self.linkName}Sensor.npy", self.values)