from collections import deque
from debug import debugmsg
from error import EntityError

class Facility:
    def __init__(self, name):
        self.name = name
        self.is_in_use = False
        self.owner = None
        self.entries = 0
        self.delaychain = deque()
    
    def seize(self, transaction):
        if self.is_in_use:
            # Facility is busy, add transaction to delay chain
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
            raise EntityError("Transaction tried to RELEASE Facility "
                f"{self.name} which it does not own")
        self.is_in_use = False
        self.owner = None
        debugmsg("facility released:", self.name)
        
        if not len(self.delaychain):
            # No transactions in delay chain
            return
        # Allow first transaction in delay chain to seize the facility
        transaction = self.delaychain.popleft()
        self._own(transaction)
        transaction.update()
