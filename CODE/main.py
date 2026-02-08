from os import path
import simulated_base
simulated_base.verify_integrity_launch() #MAY NOT BE REMOVED. MUST BE CALLED. Prevention of corruption in the program.
import MOCR
import time
import threading
import json
import sys
import subprocess
import pathlib
import simulated_base
#Message: Cubesat is not importable anymore, please load all values from Json file titled: cubesat_values.json. Thanks.
#All communication with the cubesat simulation should be done trough a json file titled :communication.json under according com title


with open(simulated_base.LAUNCH_CONFIG_PATH, 'r') as launch_config_file:
    launch_config = json.load(launch_config_file)

class simulator():
    def __init__(self, timestep, launch_config=launch_config):
        self.timestep = timestep
        self.update_thread = threading.Thread(target=self.update)
        self.launch_config = launch_config
        self.simulated_path = path.abspath("CODE/" + launch_config["simulated"] + ".py")


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
            subprocess.run([sys.executable, "CODE/launch.py"])
            self.stop()
        else:
            try:
                subprocess.run([sys.executable, self.simulated_path])
            except:
                raise Exception("Only the cubesat simulation is currently implemented")
            self.update_thread.start()



    def update(self):
        while not simulated_base.STOP_COMMAND: #while not shuting down
            pass
            input("command: MOVE: ")

        print("Update thread exiting cleanly.") #Hoppefully :)
        exit()

    def stop(self):
        print("Shutdown requested.")
        simulated_base.STOP_COMMAND = True
        self.update_thread.join()
        print("Simulation stopped.")

simulation = simulator(1) #initialize a simulator with a timestep of 1 second (This delay is for debug purposes only. Real loop will probably be 0.01 sec or less)
simulation.start() 
time.sleep(5)  # placeholder for GUI exit button
simulation.stop()