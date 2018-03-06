class TTL():
    """
    The TTL (Time To Live) is used for the cheese stack
    """
    def __init__(self, ttl):
        """
        We initialize the TTL
        """
        # We store the initial value of the TTL
        self.initial_ttl = ttl
        # We store the current TTL
        self.ttl = ttl

    def decrement(self):
        """
        We decrement the TTL
        """
        self.ttl -= 1

    def reset(self):
        """
        We reset the TTL
        """
        self.ttl = self.initial_ttl

    def is_zero(self):
        """
        We test is the TTL is dead
        """
        if(self.ttl == 0):
            return True
        return False

    def get_ttl(self):
        """
        We get the value of the TTL
        """
        return self.ttl
