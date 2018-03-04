from src.structure.ressource import Ressource

class TTL():
    def __init__(self, ttl):
        self.initial_ttl = ttl
        self.ttl = ttl

    def decrement(self):
        self.ttl -= 1

    def reset(self):
        self.ttl = self.initial_ttl

    def is_zero(self):
        if(self.ttl == 0):
            return True
        return False

    def get_ttl(self):
        return self.ttl
    
