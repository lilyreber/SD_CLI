from src.command import Command

class Parser:
    """Parser class actually just deletes space symbols from input and creates Command instance"""
    @staticmethod
    def parse(input_line):
        tokens = input_line.split()
        return Command(tokens)
