from statements import Statements
from transaction import Transaction, TransactionGenerator
from queue import Queue
from facility import Facility
from debug import debugmsg

class Simulation:
    def __init__(self):
        self.simulate = False
        self.running = False
        self.transactions = set()
        self.txn_generators = []
        self.queues = {}
        self.facilities = {}
        self.events = []
    
    def run(self, parser):
        self.parser = parser
        
        self.program = self.parser.statements
        # Create queues and facilities used in simulation
        for queue in self.parser.queues:
            self.queues[queue] = Queue(queue)
        for facility in self.parser.facilities:
            self.facilities[facility] = Facility(facility)
        
        i = 0
        while i < len(self.program):
            statement = self.program[i]
            i += 1
            if statement.type == Statements.SIMULATE:
                # Run the simulation
                self.simulate = True
            elif statement.type == Statements.GENERATE:
                # Define a transaction
                debugmsg("transaction:", statement.parameters)
                program = []
                j = i
                while True:
                    # Get transaction's program
                    block = self.program[j]
                    j += 1
                    program.append(block)
                    if block.type == Statements.TERMINATE:
                        # Transaction's program ends at TERMINATE
                        break
                txn_generator = TransactionGenerator(self,
                    statement.parameters, program)
                self.txn_generators.append(txn_generator)
                i = j
            elif statement.type == Statements.START:
                # Set number of transactions to complete
                self.term_count = statement.parameters[0]
                debugmsg("termination count:", self.term_count)
        
        # If not simulating, finish
        if not self.simulate:
            return
        
        self.time = 0
        # Add initial transaction generation events
        for txn_generator in self.txn_generators:
            txn_generator.add_next_event()
        
        # Start the simulation
        self.running = True
        while self.running:
            self.advance()
    
    def add_event(self, event):
        self.events.append(event)
        self.events.sort(key=lambda event: event.time, reverse=True)
    
    def advance(self):
        # Handle next event
        event = self.events.pop()
        self.time = event.time
        event.func()
        
        # Completed all transactions, stop running
        if self.term_count < 1:
            self.running = False
            debugmsg("finished")
