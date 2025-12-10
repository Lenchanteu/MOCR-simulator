#To debug next time: check notes

import cubesat
import time

class simulator():
    def __init__(self, timestep):
        self.timestep = timestep
class MOCR():
    def __init__(self, simulator):
        self.sim = simulator
        self.sim.start()
    
    def update(self):
        self.sim.update()
        self.check()

    def check(self):
        if self.sim.status["sim"] == "STOP":
            Exception("Capsule has died")
        
simulation = simulator(1)
simulated = cubesat.CubeSat()
operation = MOCR(simulated)
while True:
    operation.update()
    time.sleep(0.5)