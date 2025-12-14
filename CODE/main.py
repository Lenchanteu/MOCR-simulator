import cubesat
import MOCR
import time
import threading
import json

with open('SIM_FILES/launch_config.json', 'r') as launch_config_file:
    launch_config = json.load(launch_config_file)

class simulator():
    def __init__(self, timestep, launch_config=launch_config):
        self.timestep = timestep
        self.shutdown_event = threading.Event()
        self.update_thread = threading.Thread(target=self.update)
        if launch_config["simulated"] == "cubesat":
            self.simulated = cubesat.CubeSat(self.timestep)
        else:
            raise Exception("Only the cubesat simulation is currently implemented")
        self.MOCR = MOCR.MOCR(self.simulated, self.shutdown_event)


    def start(self):
        #Initializes every variables when the actual program starts
        self.simulated.start()
        self.update_thread.start()


    def update(self):
        while not self.shutdown_event.is_set(): #while not shutingdown
            self.simulated.update() 
            self.MOCR.update()
            print(self.simulated.debugMessage()) #Debug purposes only
            self.shutdown_event.wait(self.timestep)

        print("Update thread exiting cleanly.") #Hoppefully :)

    def stop(self):
        print("Shutdown requested.")
        self.shutdown_event.set()
        self.update_thread.join()
        print("Simulation stopped.")
print(f"Welcome {launch_config['username']} to the MOCR simulator! \n Please take this time to verifiy your launch configuration: \n simulated object is {launch_config['simulated']} \n you are starting a {'single' if launch_config['single_multi']==True else 'multi'}player session \n {'You are runnning a debug session \n' if launch_config['debug']==True else ''}")
simulation = simulator(1) #initialize a simulator with a timestep of 1 second (This delay is for debug purposes only. Real loop will probably be 0.01 sec or less)
simulation.start() 
time.sleep(30)  # placeholder for GUI exit button
simulation.stop()