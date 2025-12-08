#To debug next time: check notes

import random

class CubeSat():
    def __init__(self, batt_level, internal_temp, orientation, comm_status):
        self.batt_level = batt_level
        self.internal_temp = internal_temp
        self.orientation = orientation
        self.comm_status = comm_status
    
    def start(self):
        self.batt_level = random.randrange(70, 100)
        self.internal_temp = 20
        self.orientation = random.choice(["N", "S", "W", "E"])
        self.comm_status = "GOOD"
        self.message = "CLEAR"

    def update(self):
        self.batt_level -= random.randrange(0, 10)
        self.internal_temp += random.randrange(0, 10)
        self.comm_status = random.choice(["GOOD", "BAD"])
        self.checkSystem()
        self.printValues()

    def printValues(self):
        if self.comm_status == "GOOD":
            print(f'''battery level is {self.batt_level}% \n internal temperatures are {self.internal_temp} \n''')

    def checkSystem(self):
        if self.batt_level <= 0:
            self.comm_status = "BAD"
            self.message = "STOP"
    
    def debugMessage(self):
        return self.message