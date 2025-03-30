from command import StringToCommand
from src.command import Command
import argparse
import os




class Parser:
    """Parser class actually just deletes space symbols from input and creates Command instance"""
    def __init__(self):
        self.variables = os.environ.copy()
    
    def single_parse(command):
        tokens = command.split()
        command_name = tokens[0]
        if command_name == 'grep':

            parser = argparse.ArgumentParser()

            parser.add_argument("pattern", type=str, help="grep pattern")
            parser.add_argument("file", type=str, help="file to search in")
            parser.add_argument("-w", "--word", action="store_true", help="whole words only")
            parser.add_argument("-i", "--ignore-case", action="store_true", help="ignore case")
            parser.add_argument("-A", "--after", type=int, default=0, help="number of strings after match to print")

            flag_dict = parser.parse_args(' '.join(tokens[1:]))
            flag_dict = vars(flag_dict)
            args = [flag_dict['pattern'], flag_dict['file']]
            flag_dict.pop('pattern')
            flag_dict.pop('file')


        elif command_name not in StringToCommand:
            args = tokens[1:]
            return StringToCommand.external(args)
        else:
            args = tokens[1:]
            flag_dict = {}

            i = 0
            while i < len(args):
                token = args[i]

                if token.startswith('-'):
                    if '=' in token:
                        # handle --key=value
                        key, value = token.split('=', 1)
                        flag_dict[key] = value
                    elif i + 1 < len(args) and not args[i + 1].startswith('-'):
                        # handle --key value
                        flag_dict[token] = args[i + 1]
                        i += 1
                    else:
                        # flag without value (e.g. -x)
                        flag_dict[token] = None
                i += 1

        return StringToCommand[command_name](args=args, flag_dict=flag_dict)
            
            

    def parse(self, input_line):
        commands = input_line.split('|')
        if len(commands) == 1:
            if len(commands[0].split()) == 1:
                command_name = commands[0].split()[0]
                if '=' in command_name:
                    lhs, rhs = command_name.split('=')
                    self.variables[lhs.strip()] = rhs.strip()
                    return []
            return [self.single_parse(commands[0])]
        return [self.single_parse(command) for command in commands]
    


    
