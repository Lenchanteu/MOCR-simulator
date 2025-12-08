#To debug next time: check notes

import cubesat
import time


class MOCR():
    def __init__(self, simulator):
        self.sim = simulator
        self.sim.start()
    
    def update(self):
        self.sim.update()
        self.cap_message = self.sim.message()
        self.check()

    def check(self):
        if self.cap_message == "STOP":
            Exception("Capsule has died")
        
simulator = cubesat.CubeSat(0, 0, 0, 0)
operation = MOCR(simulator)
while True:
    operation.update()
    time.sleep(0.5)