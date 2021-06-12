from collections import deque
from .debug import debugmsg
from .error import simulation_error

class Facility:
    def __init__(self, name):
        self.name = name
        self.is_in_use = False
        self.owner = None
        self.entries = 0
        self.delaychain = deque()
    
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
        debugmsg("facility seized:", self.name)
    
    def release(self, transaction):
        if transaction is not self.owner:
            simulation_error(self.simulation.parser.infile,
                transaction.current_linenum,
                "Transaction tried to RELEASE Facility "
                f"\"{self.name}\" which it does not own")
        self.is_in_use = False
        self.owner = None
        debugmsg("facility released:", self.name)
        
        if not len(self.delaychain):
            # No Transactions in Delay Chain
            return
        # Allow first Transaction in Delay Chain to seize the Facility
        transaction = self.delaychain.popleft()
        self._own(transaction)
        transaction.update()
