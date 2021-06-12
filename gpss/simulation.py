from .statement import Statement, StatementType, BLOCKS
from .transaction import Transaction, TransactionGenerator
from .storage import Storage
from .report import createReport
from .debug import debugmsg
from .error import simulation_error

class Simulation:
    def __init__(self):
        self.running = False
        self.current_statement = None
        self.reports = []
        self.completed = 0
    
    def run(self, parser):
        self.parser = parser
        if self.parser.error_count > 0:
            # Couldn't parse the entire program successfully
            simulation_error(self.parser.infile, None,
                "Can't run a GPSS program with parser errors")
        
        self.program = self.parser.statements
        self.labels = self.parser.labels
        
        self.initialize(first=True)
        
        # No START Command
        if self.current_statement is None:
            simulation_error(self.parser.infile, None,
                "Program contains no START Command")
        
        while self.current_statement < len(self.program):
            statement = self.program[self.current_statement]
            self.current_statement += 1
            
            # Start the simulation
            if statement.type is StatementType.START:
                # Set number of Transactions to complete
                self.term_count = statement.operands[0]
                debugmsg("termination count:", self.term_count)
                
                # Prime Transaction generators
                for txn_generator in self.txn_generators:
                    txn_generator.prime()
                
                self.running = True
                while self.running:
                    self.advance()
                
                self.completed += 1
                self.reports.append(createReport(self))
            
            elif statement.type is StatementType.END:
                return True
            
            elif statement.type is StatementType.CLEAR:
                self.initialize(first=False)
            
            # Replace an existing Block
            elif statement.type in BLOCKS:
                if statement.label is None:
                    simulation_error(self.parser.infile,
                        statement.linenum,
                        "Replacement Block has no label")
                
                old_block = self.labels[statement.label]
                
                # GENERATE Blocks must be replaced with GENERATE Blocks
                if (old_block.type is StatementType.GENERATE
                        and statement.type is not StatementType.GENERATE):
                    simulation_error(self.parser.infile,
                        statement.linenum, "A GENERATE Block must be "
                        "replaced with a GENERATE Block")
                
                debugmsg("replace:", old_block.linenum,
                    statement.linenum)
                
                # Take the old Block's place in the program
                self.program[old_block.number] = statement
                statement.linenum = old_block.linenum
                statement.number = old_block.number
        
        # Ran past end
        simulation_error(self.parser.infile, None,
            "Ran past the end of the program (missing END Command?)")
    
    def initialize(self, first):
        # Clear leftover Entities
        self.transactions = set()
        self.txn_generators = []
        self.queues = {}
        self.facilities = {}
        self.storages = {}
        self.events = []
        
        # Reset Clock
        self.time = 0
        
        for statement in self.program:
            # Define a Transaction
            if statement.type is StatementType.GENERATE:
                debugmsg("transaction:", statement.operands)
                txn_generator = TransactionGenerator(self,
                    statement.number, statement.operands)
                self.txn_generators.append(txn_generator)
            
            # Define a Storage's capacity
            elif statement.type is StatementType.STORAGE:
                self.storages[statement.label] = Storage(
                    statement.label, statement.operands[0])
                debugmsg("storage:", statement.label,
                    statement.operands[0])
            
            elif statement.type is StatementType.START:
                # First START Command, set as current statement
                if first and self.current_statement is None:
                    self.current_statement = statement.number
                break
    
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
