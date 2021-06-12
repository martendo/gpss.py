from collections import deque
from .debug import debugmsg
from .error import simulation_error

class Storage:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.available = self.capacity
        self.entries = 0
        self.max = 0
        self.delaychain = deque()
    
    @property
    def content(self):
        return self.capacity - self.available
    
    def __repr__(self):
        return f"Storage({self.capacity}, {self.content}, {self.available})"
    
    def enter(self, transaction, demand):
        if demand > self.capacity:
            simulation_error(self.simulation.parser.infile,
                transaction.current_linenum,
                f"Storage \"{self.name}\" does not have the "
                f"capacity to satisfy the demand of {demand} "
                f"(capacity {self.capacity})")
        elif demand > self.available:
            # Storage cannot satisfy demand, add Transaction to delay
            # chain
            self.delaychain.append((transaction, demand))
            return False
        # Storage has sufficient availability
        self._use(demand)
        return True
    
    def _use(self, demand):
        self.available -= demand
        if self.content > self.max:
            self.max = self.content
        self.entries += demand
        debugmsg("storage entered:", self.name, demand)
    
    def leave(self, transaction, units):
        self.available += units
        if self.available > self.capacity:
            simulation_error(self.simulation.parser.infile,
                transaction.current_linenum,
                f"LEAVE resulted in more available units "
                f"than capacity in Storage \"{self.name}\" "
                f"(capacity {self.capacity}, available {self.available})")
        debugmsg("storage left:", self.name, units)
        
        if not len(self.delaychain):
            # No Transactions in Delay Chain
            return
        # Allow first Transaction with demand that can be satisfied in
        # Delay Chain to enter the Storage
        for i, (transaction, demand) in enumerate(self.delaychain):
            if demand <= self.available:
                break
        del self.delaychain[i]
        self._use(demand)
        transaction.update()
