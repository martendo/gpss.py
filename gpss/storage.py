from .delay_chain import DelayChain
from .debug import debugmsg
from .error import simulation_error

class Storage:
    def __init__(self, simulation, name, capacity):
        self.simulation = simulation
        self.name = name
        
        self.capacity = capacity
        self.available = self.capacity
        self.entries = 0
        self.max_content = 0
        self.utilization = 0
        self.delaychain = DelayChain()
        self.demandmap = {}
        
        self.last_change = 0
    
    @property
    def content(self):
        return self.capacity - self.available
    
    def __repr__(self):
        return f"Storage({self.capacity}, {self.content}, {self.available})"
    
    def change(self):
        self.utilization += (
            (self.simulation.time - self.last_change) * self.content)
        self.last_change = self.simulation.time
    
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
            self.delaychain.append(transaction)
            self.demandmap[transaction] = demand
            return False
        # Storage has sufficient availability
        self._use(demand)
        return True
    
    def _use(self, demand):
        self.change()
        self.available -= demand
        if self.content > self.max_content:
            self.max_content = self.content
        self.entries += demand
        debugmsg("storage entered:", self.name, demand)
    
    def leave(self, transaction, units):
        self.change()
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
        for i, transaction in enumerate(self.delaychain):
            demand = self.demandmap[transaction]
            if demand <= self.available:
                break
        else:
            # No Transaction's demand can be satisfied
            return
        del self.delaychain[i]
        del self.demandmap[transaction]
        self._use(demand)
        transaction.update()
