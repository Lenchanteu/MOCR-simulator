#To debug next time: check notes

import random

class CubeSat():
    def __init__(self, timestep=1):
        self.comm_status = "UNKNOWN"
        self.message = "UNKNOWN"
        self.batt_level = 100  # percentage
        self.internal_temp = 25  # Celsius
        self.orientation = "N"  # N, S, W, E
        self.status = {
            "comm": self.comm_status,
            "sim": self.message
        }
        self.start_ok = False
        self.timestep =timestep  # seconds
    
    def start(self):
        self.batt_level = random.randrange(70, 100)
        self.internal_temp = 20
        self.orientation = random.choice(["N", "S", "W", "E"])
        self.comm_status = "GOOD"
        self.message = "CLEAR"
        #location variable: [x, y, z]
        self.location = [0, 0, 0]
        self.rotation = [0, 0, 0]
        self.power = 0
        self.batt_efficiency = 0.05
        self.start_ok = True

    def update(self):
        if self.start_ok != True:
            raise Exception("Simulated object was not started, please verify the configuration.")
        #self.batt_level -= random.randrange(0, 10) /used for debug purposes
        #self.internal_temp += random.randrange(-10, 10) /same
        #self.comm_status = random.choice(["GOOD", "BAD"]) /same
        self.checkSystem()
        
    def checkSystem(self):
        if self.batt_level <= 0:
            self.comm_status = "BAD"
            self.message = "STOP"
    
    def debugMessage(self):
        return self.message
    

    def locationUpdater(self, rotation, power, time): #time should be in second, rotation in degrees, power in percent
        if self.batt_level >= 10:
            self.rotation += rotation
            self.power=power
            self.displacement_x = self.rotation[0]*self.power
            self.displacement_y = self.rotation[1]*self.power
            self.displacement_z = self.rotation[2]*self.power

            self.move_cycles = time/self.timestep
    
    def mover(self):
        self.location[0] += self.displacement_x
        self.location[1] += self.displacement_y
        self.location[2] += self.displacement_z

        self.batt_level -= ((self.displacement_x + self.displacement_y + self.displacement_z) * self.batt_efficiency)

