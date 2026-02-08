## CODE/cubesat.py
#connected to main.py by import
import simulated_base
simulated_base.verify_integrity_launch() #MAY NOT BE REMOVED. MUST BE CALLED. Prevention of corruption in the program.
import random
import time
import threading
import json
import sys


class CubeSat():
    def __init__(self, timestep=1, batt_level=100, internal_temp=25, rotation=[0,0,0], location=[0,0,0]):
        self.COMMAND_TABLE = {
                "MOVE": {"name": self.move,
                        "args": 
                        ["rotation",
                        "power", 
                        "duration",]
                        }, 
                "DEBUG": 
                {"name": self.debugMessage, 
                "args": []},
                "NONE":
                {"name": simulated_base.noop,
                "args": []},
                "STOP": 
                {"name": self.__stop, 
                 "args": []}
                        }
        
        # Currently "random" initial values for testing purposes
        self.batt_level = batt_level  # percentage
        self.internal_temp = internal_temp  # Celsius
        self.rotation = rotation
        self.location = location
        self.comm_status = 0
        self.message = 0
        self.start_ok = False
        self.timestep = timestep  # in seconds
        self.log_filling_thread = threading.Thread(target=self.logfiling)
        self.stop_signal = False
    
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
        self.cycle = 0

        self.log_filling_thread.start()
        self.start_ok = True


    def update(self):
        #self.batt_level -= random.randrange(0, 10) ,used for debug purposes
        #self.internal_temp += random.randrange(-10, 10) ,same
        #self.comm_status = random.choice(["GOOD", "BAD"]) ,same
        self.sim_state, self.timestep = simulated_base.receiveData()  #type: ignore need to find a way to only have sim_state
        self.command, self.args = simulated_base.receiveCommand() # type: ignore
        self.executeCommand()
        simulated_base.sendData(self.batt_level, self.internal_temp, self.rotation, self.location, self.comm_status, self.message)
        self.checkSystem()
        self.cycle += 1

    def __stop(self):
        simulated_base.STOP_COMMAND = True
        self.log_filling_thread.join()
    def checkSystem(self):
        if self.batt_level <= 0:
            self.comm_status = "BAD"
            self.message = "STOP"
        if self.sim_state == 0:
            self.__stop()

    
    def executeCommand(self):
         command = simulated_base.dispatchCommands(self.COMMAND_TABLE, self.command, self.args, self)
         if command == None:
             return
         if command: 
             command()


    def debugMessage(self):
        return self.batt_level,self.internal_temp,self.rotation,self.location,self.comm_status,self.message,self.timestep, self.cycle
    
    def move(self, rotation, power, duration):
        self.rotation[0] += rotation[0]
        self.rotation[1] += rotation[1]
        self.rotation[2] += rotation[2]
        self.batt_level, self.location = simulated_base.locationUpdater(self.rotation, power, duration, self.batt_level, self.timestep, self.location, self.batt_efficiency)
    def logfiling(self):
        while not simulated_base.STOP_COMMAND:
            
            with open(simulated_base.LOG_FILE_PATH, 'a') as log_file:
                json_data = {
                    "time": time.time(),
                    "batt_level": self.batt_level,
                    "internal_temp": self.internal_temp,
                    "rotation": self.rotation,
                    "location": self.location,
                    "comm_status": self.comm_status,
                    "message": self.message,
                    "timestep": self.timestep,
                    "cycle": self.cycle,
                }
                json.dump(json_data, log_file)
            time.sleep(10 * self.timestep)

cubesat = CubeSat()
cubesat.start()
next_tick = time.time()
while not simulated_base.STOP_COMMAND:
    cubesat.update()
    next_tick += cubesat.timestep
    time.sleep(max(0, next_tick - time.time()))