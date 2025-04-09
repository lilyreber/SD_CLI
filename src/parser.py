from command import CommandFactory
import argparse
import os

from environment import Environment


class Parser:
    """Parser class splits line by |, parses name, flags and args and returns list[Command]"""

    @staticmethod
    def single_parse(command):
        tokens = command.split()
        if not tokens:
            return None
        command_name = tokens[0]
        if command_name == 'grep':

            parser = argparse.ArgumentParser()

            parser.add_argument("-w", "--word", action="store_true", help="whole words only")
            parser.add_argument("-i", "--ignore-case", action="store_true", help="ignore case")
            parser.add_argument("-A", "--after", type=int, help="number of strings after match to print")
            parser.add_argument("pattern", type=str, help="pattern to search for")
            parser.add_argument("file", type=str, help="file to search in")

            parse_string = ' '.join(tokens[1:])
            flag_dict = parser.parse_args(parse_string.split())
            flag_dict = vars(flag_dict)
            pattern = flag_dict["pattern"].strip('"')

            args = [pattern, flag_dict['file']]
            flag_dict.pop('pattern')
            flag_dict.pop('file')


        elif not CommandFactory.is_enum_value(command_name.upper()):
            return CommandFactory.build_external(tokens)
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

        return CommandFactory.build_command(command_name.upper(), args=args, flag_dict=flag_dict)

    @staticmethod
    def parse(input_line, env: Environment):
        substitute_line = env.substitute_vars(input_line)
        commands = substitute_line.split('|')

        if not commands:
            return []
        if len(commands) == 1:
            if len(commands[0].split()) == 1:
                command_name = commands[0].split()[0]
                if '=' in command_name:
                    lhs, rhs = command_name.split('=')
                    env.set_variable(lhs.strip(), rhs.strip())
                    return []

        return [Parser.single_parse(command) for command in commands]
