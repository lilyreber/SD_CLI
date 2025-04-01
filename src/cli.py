from parser import Parser
from pipeline import Pipeline
import os

class CLI:
    
    prev_status_code = 0

    def run(self):
        parser = Parser()
        pipeline = Pipeline()

        while True:
            try:
                input_line = input("cli> ")
                # Commands - array of Command objects
                commands = parser.parse(input_line) 

                prev_status_code = pipeline.execute(commands)
            except KeyboardInterrupt:
                # Handle Ctrl+C interruption gracefully
                print("\nUse 'exit' to quit.", file=os.stdout)