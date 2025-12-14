## CODE/cubesat.py
#connected to main.py by import

import random

class CubeSat():
    def __init__(self, timestep=1):
        # Currently "random" initial values for testing purposes
        self.comm_status = "UNKNOWN"
        self.message = "UNKNOWN"
        self.batt_level = 100  # percentage
        self.internal_temp = 25  # Celsius
        self.orientation = "N"  # N, S, W, E
        #
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
        self.orientation = random.choice(["N", "S", "W", "E"])
        self.comm_status = "GOOD"
        self.message = "CLEAR"
        #Movement related variables, should reflect location on a 3d axis
        self.location = [0, 0, 0]
        self.rotation = [0, 0, 0]
        #Must be 0 at start
        self.power = 0
        self.batt_efficiency = 0.05 #to replace by actual values in NASA/ESA documentation
        #Must be kept here at the end, indicates proper initialization
        self.start_ok = True

    def update(self):
        if self.start_ok != True:
            raise Exception("Simulated object was not started, please verify the configuration.")
        #self.batt_level -= random.randrange(0, 10) ,used for debug purposes
        #self.internal_temp += random.randrange(-10, 10) ,same
        #self.comm_status = random.choice(["GOOD", "BAD"]) ,same
        self.checkSystem()
        
    def checkSystem(self):
        if self.batt_level <= 0:
            self.comm_status = "BAD"
            self.message = "STOP"

        self.status["comm"] = self.comm_status
        self.status["sim"] = self.message

    def debugMessage(self):
        return self.message
    

    def locationUpdater(self, rotation, power, time): #time should be in second, rotation in degrees, power in percent
        if self.batt_level >= 10: #minimum battery level to perform any movement
            self.rotation += rotation #updates rotation based on input
            self.power=power
            #Calculate displacement on each axis
            self.displacement_x = self.rotation[0]*self.power
            self.displacement_y = self.rotation[1]*self.power
            self.displacement_z = self.rotation[2]*self.power
            #calculate number of cycles to perform based on inputed time and main timestep
            self.move_cycles = time/self.timestep
    
    def mover(self): #actual movement function
        self.location[0] += self.displacement_x
        self.location[1] += self.displacement_y
        self.location[2] += self.displacement_z

        self.batt_level -= ((self.displacement_x + self.displacement_y + self.displacement_z) * self.batt_efficiency) #not shure about this formula, to be checked with documentation

