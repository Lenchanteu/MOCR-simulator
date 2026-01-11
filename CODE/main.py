import MOCR
import time
import threading
import json
import sys
import subprocess
import pathlib
#Message: Cubesat is not importable anymore, please load all values from Json file titled: cubesat_values.json. Thanks.
#All communication with the cubesat simulation should be done trough a json file titled :communication.json under according com title
User_Home_Path = str(pathlib.Path.home())
with open(f'{User_Home_Path}\\MOCRSim\\launch_config.json', 'r') as launch_config_file:
    launch_config = json.load(launch_config_file)

class simulator():
    def __init__(self, timestep, launch_config=launch_config):
        self.timestep = timestep
        self.shutdown_event = threading.Event()
        self.update_thread = threading.Thread(target=self.update)
        #if launch_config["simulated"] == "cubesat":
        #    self.simulated = cubesat.CubeSat(self.timestep)
        #else:
        #    raise Exception("Only the cubesat simulation is currently implemented")
        #self.MOCR = MOCR.MOCR(self.simulated, self.shutdown_event)


    def start(self):
        #Initializes every variables when the actual program starts
        print(f"Welcome {launch_config['username']} to the MOCR simulator! \n Please take this time to verifiy your launch configuration: \n simulated object is {launch_config['simulated']} \n you are starting a {'single' if launch_config['single_multi']==True else 'multi'}player session \n {'You are runnning a debug session \n' if launch_config['debug']==True else ''}")
        go_ahead = str.lower(input("Please confirm that the info above are correct: True/False: "))
        if go_ahead == "true":
            go_ahead = True
        else:
            go_ahead = False
        if go_ahead != True:
            print("Misconfigurations, going back to launch screen. Please wait...")
            self.stop()
            subprocess.run([sys.executable, "CODE/launch.py"])
        else:
            #self.simulated.start()
            self.update_thread.start()



    def update(self):
        while not self.shutdown_event.is_set(): #while not shutingdown
            #self.simulated.update() 
            #self.MOCR.update()
            #print(self.simulated.debugMessage()) #Debug purposes only
            self.shutdown_event.wait(self.timestep)

        print("Update thread exiting cleanly.") #Hoppefully :)

    def stop(self):
        print("Shutdown requested.")
        self.shutdown_event.set()
        self.update_thread.join()
        print("Simulation stopped.")

simulation = simulator(1) #initialize a simulator with a timestep of 1 second (This delay is for debug purposes only. Real loop will probably be 0.01 sec or less)
simulation.start() 
time.sleep(30)  # placeholder for GUI exit button
simulation.stop()