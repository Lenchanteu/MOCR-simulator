## CODE/cubesat.py
#connected to main.py by import

import random
from time import sleep
import simulated_base
import json
import sys

class CubeSat():
    def __init__(self, timestep=1, batt_level=100, internal_temp=25, rotation=[0,0,0], location=[0,0,0]):
        # Currently "random" initial values for testing purposes
        self.batt_level = batt_level  # percentage
        self.internal_temp = internal_temp  # Celsius
        self.rotation = rotation
        self.location = location
        
        self.status = {
            "comm": self.comm_status,
            "sim": self.message
        }
        self.start_ok = False
        self.timestep = timestep  # in seconds
    
    def start(self):
        #Initializes variables when called, variables are randomized for testing purposes
        self.batt_level = random.randrange(70, 100)
        self.internal_temp = 20
        self.comm_status = "GOOD"
        self.message = "CLEAR"
        #Movement related variables, should reflect location on a 3d axis
        self.location = [0, 0, 0]
        self.rotation = [0, 0, 0]
        self.batt_efficiency = 0.05 #to replace by actual values in NASA/ESA documentation
        #Must be kept here at the end, indicates proper initialization
        self.start_ok = True


    def update(self):
        #self.batt_level -= random.randrange(0, 10) ,used for debug purposes
        #self.internal_temp += random.randrange(-10, 10) ,same
        #self.comm_status = random.choice(["GOOD", "BAD"]) ,same
        self.sim_state, self.timestep = simulated_base.receiveData() # type: ignore #need to find a way to only have sim_state
        self.command = simulated_base.receiveCommand()
        simulated_base.sendData(self.batt_level, self.internal_temp, self.rotation, self.location, self.comm_status, self.message)
        self.checkSystem()
        
    def checkSystem(self):
        if self.batt_level <= 0:
            self.comm_status = "BAD"
            self.message = "STOP"
        if self.sim_state == 0:
            self.__stop()

        self.status["comm"] = self.comm_status
        self.status["sim"] = self.message

    def debugMessage(self):
        return self.message
    
    def move(self, rotation, power, duration):
        self.rotation += rotation
        self.batt_level, self.location = simulated_base.locationUpdater(self.rotation, power, duration, self.batt_level, self.timestep, self.location, self.batt_efficiency)
    
    
    
  
    

    
    def __stop(self):
        sys.exit(0)

cubesat = CubeSat()
while True:
    cubesat.update()
    sleep(cubesat.timestep)