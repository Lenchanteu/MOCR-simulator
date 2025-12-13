#To debug next time: check notes

import cubesat
import MOCR
import time
import threading

class simulator():
    def __init__(self, timestep):
        self.timestep = timestep
        self.active = False
        self.update_thread = threading.Thread(target=self.update)
        self.simulated = cubesat.CubeSat(self.timestep)
        self.MOCR = MOCR.MOCR(self.simulated)



    def start(self):
        self.MOCR.sim.start()
        #Must be called at the end of start to avoid non initialized variable errors
        self.active = True
        self.update_thread.start()
        return 0


    def update(self):
        while self.active == True:
            self.simulated.update()
            self.MOCR.update()
            print(self.simulated.debugMessage())
            time.sleep(self.timestep)
        self.stop()

    def stop(self):
        #Change later to proper stop procedures :)
        raise Exception("Simulation has stopped")

simulation = simulator(1)
simulation.start()
time.sleep(30)
simulation.active = False