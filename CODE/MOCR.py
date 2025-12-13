class MOCR():
    def __init__(self, simulated):
        self.sim = simulated
    
    def update(self):
        self.check()

    def check(self):
        if self.sim.status["sim"] == "STOP":
            Exception("Capsule has died")
        