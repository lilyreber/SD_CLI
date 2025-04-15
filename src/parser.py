from command import CommandFactory
import argparse
import os
import sys
import shlex
from environment import Environment


class Parser:
    """Parser class splits line by |, parses name, flags and args and returns list[Command]"""

    @staticmethod
    def single_parse(command):
        try:
            tokens = shlex.split(command)
            if not tokens:
                return None

            command_name = tokens[0]

            # # Special handling for grep
            if command_name == 'grep':
                parser = argparse.ArgumentParser(prog="grep", add_help=False)

                parser.add_argument("-w", "--word", action="store_true", help="whole words only")
                parser.add_argument("-i", "--ignore-case", action="store_true", help="ignore case")
                parser.add_argument("-A", "--after", type=int, help="number of strings after match to print")
                parser.add_argument("pattern", type=str, help="pattern to search for")
                parser.add_argument("file", type=str, nargs="?",help="file to search in", default=None)

                try:
                    parse_string = ' '.join(tokens[1:])
                    flag_dict = parser.parse_args(parse_string.split())
                    flag_dict = vars(flag_dict)

                    pattern = flag_dict["pattern"].strip('"')
                    args = [pattern, flag_dict['file']]
                    flag_dict.pop('pattern')
                    flag_dict.pop('file')
                except SystemExit:
                    # argparse throws this on bad args
                    print("Error: invalid arguments for grep.", file=sys.stderr)
                    return None

            elif not CommandFactory.is_enum_value(command_name.upper()):
                return CommandFactory.build_external(tokens)

            else:
                args = tokens[1:]
                flag_dict = {}
                new_args = []
                i = 0
                while i < len(args):
                    token = args[i]
                    if token.startswith('-'):
                        if '=' in token:
                            key, value = token.split('=', 1)
                            flag_dict[key] = value
                        elif i + 1 < len(args) and not args[i + 1].startswith('-'):
                            flag_dict[token] = args[i + 1]
                            i += 1
                        else:
                            flag_dict[token] = None
                    else:
                        new_args.append(token)
                    i += 1
                args = new_args

            return CommandFactory.build_command(command_name.upper(), args=args, flag_dict=flag_dict)

        except Exception as e:
            print(f"Error while parsing command: {e}", file=sys.stderr)
            return None

    @staticmethod
    def parse(input_line, env: Environment):
        try:
            substitute_line = env.substitute_vars(input_line)
            commands = substitute_line.split('|')

            if not commands:
                return []

            # Handle variable assignment like x=1
            if len(commands) == 1:
                stripped = commands[0].strip()
                if len(stripped.split()) == 1 and '=' in stripped:
                    parts = stripped.split('=', 1)
                    if len(parts) == 2:
                        lhs, rhs = parts
                        lhs, rhs = lhs.strip(), rhs.strip()
                        if lhs:
                            env.set_variable(lhs, rhs)
                        else:
                            print("Invalid variable assignment.", file=sys.stderr)
                    else:
                        print("Invalid variable assignment.", file=sys.stderr)
                    return []

            return [cmd for cmd in (Parser.single_parse(command.strip()) for command in commands)]

        except Exception as e:
            print(f"Error while parsing line: {e}", file=sys.stderr)
            return []
