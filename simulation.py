from statements import Statements
from transaction import Transaction, TransactionGenerator
from storage import Storage
from debug import debugmsg

class Simulation:
    def __init__(self):
        self.running = False
        self.transactions = set()
        self.txn_generators = []
        self.queues = {}
        self.facilities = {}
        self.storages = {}
        self.events = []
    
    def run(self, parser):
        self.parser = parser
        if not self.parser.found_simulate:
            # No SIMULATE Block -> don't run the simulation
            return False
        
        self.program = self.parser.statements
        # Create Storages used in simulation
        for storage, capacity in self.parser.storages:
            self.storages[storage] = Storage(storage, capacity)
        
        i = 0
        while i < len(self.program):
            statement = self.program[i]
            i += 1
            if statement.type == Statements.GENERATE:
                # Define a Transaction
                debugmsg("transaction:", statement.operands)
                program = []
                j = i
                while True:
                    # Get Transaction's program
                    block = self.program[j]
                    j += 1
                    program.append(block)
                    if block.type == Statements.TERMINATE:
                        # Transaction's program ends at TERMINATE
                        break
                txn_generator = TransactionGenerator(self,
                    statement.linenum, program, statement.operands)
                self.txn_generators.append(txn_generator)
                i = j
            elif statement.type == Statements.START:
                # Set number of Transactions to complete
                self.term_count = statement.operands[0]
                debugmsg("termination count:", self.term_count)
        
        self.time = 0
        # Prime Transaction generators
        for txn_generator in self.txn_generators:
            txn_generator.prime()
        
        # Start the simulation
        self.running = True
        while self.running:
            self.advance()
        
        return True
    
    def add_event(self, event):
        self.events.append(event)
        self.events.sort(key=lambda event: event.time, reverse=True)
    
    def advance(self):
        # Handle next event
        try:
            event = self.events.pop()
        except IndexError:
            self.running = False
            return
        self.time = event.time
        event.func()
        
        # Completed all Transactions, stop running
        if self.term_count < 1:
            self.running = False
