import shlex

from src.command import Command


class Parser:
    @staticmethod
    def parse(input_line):
        tokens = shlex.split(input_line)
        return Command(tokens)
