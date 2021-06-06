from collections import deque
from debug import debugmsg

class Facility:
    def __init__(self, name):
        self.name = name
        self.is_in_use = False
        self.entries = 0
        self.delaychain = deque()
    
    def seize(self, transaction):
        if self.is_in_use:
            # Facility is busy, add transaction to delay chain
            self.delaychain.append(transaction)
            transaction.delaying = True
            return
        # Facility is available
        self._use()
    
    def _use(self):
        self.is_in_use = True
        self.entries += 1
        debugmsg("facility seized:", self.name)
    
    def release(self):
        self.is_in_use = False
        debugmsg("facility released:", self.name)
        
        if not len(self.delaychain):
            # No transactions in delay chain
            return
        # Allow first transaction in delay chain to seize the facility
        self.delaychain.popleft().delaying = False
        self._use()
