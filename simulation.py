from transaction import Transaction, TransactionGenerator
from debug import debugmsg

class Simulation:
    def __init__(self):
        self.simulate = False
        self.running = False
        self.transactions = set()
        self.txn_generators = []
        self.queues = {}
        self.time = 0
    
    def run(self, parser):
        self.program = parser.statements
        # Create queues used in simulation
        for queue in parser.queues:
            self.queues[queue] = 0
        
        i = 0
        while i < len(self.program):
            statement = self.program[i]
            i += 1
            if statement[0] == "SIMULATE":
                # Run the simulation
                self.simulate = True
            elif statement[0] == "GENERATE":
                # Define a transaction
                debugmsg("transaction:", statement)
                program = []
                j = i
                while True:
                    # Get transaction's program
                    block = self.program[j]
                    j += 1
                    program.append(block)
                    if block[0] == "TERMINATE":
                        # Transaction's program ends at TERMINATE
                        break
                txn_generator = TransactionGenerator(self,
                    statement[1], program)
                self.txn_generators.append(txn_generator)
                i = j
            elif statement[0] == "START":
                # Set number of transactions to complete
                self.term_count = int(statement[1][0])
                debugmsg("termination count:", self.term_count)
        
        # Set initial transaction generation times
        for txn_generator in self.txn_generators:
            txn_generator.update_nexttime()
        
        # Start the simulation
        self.running = True
        while self.running:
            self.advance()
    
    def advance(self):
        # Generate any new transactions as necessary
        for txn_generator in self.txn_generators:
            txn_generator.update()
        
        # Run transaction programs
        for transaction in tuple(self.transactions):
            transaction.update()
            # Completed all transactions, stop running
            if self.term_count < 1:
                self.running = False
                break
        
        # Move through time
        self.time += 1
