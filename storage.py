from collections import deque
from debug import debugmsg
from error import SimulationError

class Storage:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.available = self.capacity
        self.entries = 0
        self.max = 0
        self.delaychain = deque()
    
    def enter(self, transaction, demand):
        if demand > self.capacity:
            raise SimulationError(f"Storage {self.name} does not have "
                f"the capacity to satisfy the demand of {demand} "
                f"(capacity {self.capacity})")
        elif demand > self.available:
            # Storage cannot satisfy demand, add transaction to delay
            # chain
            self.delaychain.append((transaction, demand))
            return False
        # Storage has sufficient availability
        self._use(demand)
        return True
    
    def _use(self, demand):
        self.available -= demand
        used = self.capacity - self.available
        if used > self.max:
            self.max = used
        self.entries += demand
        debugmsg("storage entered:", self.name, demand)
    
    def leave(self, units):
        self.available += units
        if self.available > self.capacity:
            raise SimulationError(f"LEAVE resulted in more available "
                f"units than capacity in Storage {self.name} "
                f"(capacity {self.capacity}, available {self.available})")
        debugmsg("storage left:", self.name, units)
        
        if not len(self.delaychain):
            # No transactions in delay chain
            return
        # Allow first transaction with demand that can be satisfied in
        # delay chain to enter the storage
        for i, (transaction, demand) in enumerate(self.delaychain):
            if demand <= self.available:
                break
        del self.delaychain[i]
        self._use(demand)
        transaction.update()
