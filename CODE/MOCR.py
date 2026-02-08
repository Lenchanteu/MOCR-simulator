## CODE/MOCR.py
#Connected to main.py by import
import simulated_base

class MOCR():
    def __init__(self, simulated, shutdown_event):
        self.sim = simulated
        self.shutdown_event = shutdown_event
    
    def update(self):
        self.check()

    def check(self):
        if self.sim.status["sim"] == "STOP":
            print("MOCR: Capsule has died.")

simulated_base.verify_integrity_launch() #MAY NOT BE REMOVED. MUST BE CALLED. Prevention of corruption in the program.