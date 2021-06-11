from .statements import Statements
from .transaction import Transaction, TransactionGenerator
from .storage import Storage
from .debug import debugmsg
from .error import simulation_error

class Simulation:
    def __init__(self):
        self.running = False
        self.current_statement = None
        self.transactions = set()
        self.txn_generators = []
        self.queues = {}
        self.facilities = {}
        self.storages = {}
        self.events = []
    
    def run(self, parser):
        self.parser = parser
        if self.parser.error_count > 0:
            # Couldn't parse the entire program successfully
            simulation_error(self.parser.inputfile, None,
                "Can't run a GPSS program with parser errors")
        
        self.program = self.parser.statements
        # Create Storages used in simulation
        for storage, capacity in self.parser.storages:
            self.storages[storage] = Storage(storage, capacity)
        
        for num, statement in enumerate(self.program):
            if statement.type == Statements.GENERATE:
                # Define a Transaction
                debugmsg("transaction:", statement.operands)
                txn_generator = TransactionGenerator(self, num,
                    statement.operands)
                self.txn_generators.append(txn_generator)
            elif statement.type == Statements.START:
                # First START Command, set as current statement
                if self.current_statement is None:
                    self.current_statement = num
        
        # No START Command
        if self.current_statement is None:
            simulation_error(self.parser.inputfile, None,
                "Program contains no START Command")
        
        self.time = 0
        
        while self.current_statement < len(self.program):
            statement = self.program[self.current_statement]
            self.current_statement += 1
            
            if statement.type == Statements.START:
                # Set number of Transactions to complete
                self.term_count = statement.operands[0]
                debugmsg("termination count:", self.term_count)
                
                # Start the simulation
                
                # Prime Transaction generators
                for txn_generator in self.txn_generators:
                    txn_generator.prime()
                
                self.running = True
                while self.running:
                    self.advance()
            
            elif statement.type == Statements.END:
                return True
        
        # Ran past end
        simulation_error(self.parser.inputfile, None,
            "Ran past the end of the program (missing END Command?)")
    
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
