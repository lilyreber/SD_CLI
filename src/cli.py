from parser import Parser
from pipeline import Pipeline
from environment import Environment

import sys


class CLI:
    __prev_status_code = 0

    def __init__(self):
        self.__parser = Parser()
        self.__pipeline = Pipeline()
        self.__env = Environment()

    def run(self):

        while True:
            try:
                input_line = input("cli> ")
                # Commands - array of Command objects
                commands = self.__parser.parse(input_line, self.__env)

                self.__prev_status_code = self.__pipeline.execute(commands)
            except KeyboardInterrupt:
                # Handle Ctrl+C interruption gracefully
                print("\nUse 'exit' to quit.", file=sys.stdout)
