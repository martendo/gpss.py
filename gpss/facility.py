from .delay_chain import DelayChain
from .debug import debugmsg
from .error import simulation_error

class Facility:
    def __init__(self, simulation, name):
        self.simulation = simulation
        self.name = name
        
        self.is_in_use = False
        self.owner = None
        self.delaychain = DelayChain()
        self.reset()
    
    def reset(self):
        self.entries = 0
        self.utilization = 0
    
    @property
    def average_utilization(self):
        try:
            return self.utilization / self.simulation.rel_time
        except ZeroDivisionError:
            return 0
    @property
    def average_time(self):
        try:
            return self.utilization / self.entries
        except ZeroDivisionError:
            return -1
    
    def __repr__(self):
        return f"Facility({self.is_in_use})"
    
    def seize(self, transaction):
        if self.is_in_use:
            # Facility is busy, add Transaction to Delay Chain
            self.delaychain.append(transaction)
            return False
        # Facility is available
        self._own(transaction)
        return True
    
    def _own(self, transaction):
        self.is_in_use = True
        self.owner = transaction
        self.entries += 1
        self.last_seize = self.simulation.time
        debugmsg("facility seized:", self.name)
    
    def release(self, transaction):
        if transaction is not self.owner:
            simulation_error(self.simulation.parser.infile,
                transaction.current_linenum,
                "Transaction tried to RELEASE Facility "
                f"\"{self.name}\" which it does not own")
        self.is_in_use = False
        self.owner = None
        self.utilization += self.simulation.time - self.last_seize
        debugmsg("facility released:", self.name)
        
        if not len(self.delaychain):
            # No Transactions in Delay Chain
            return
        # Allow first Transaction in Delay Chain to seize the Facility
        transaction = self.delaychain.popleft()
        self._own(transaction)
        transaction.update()
