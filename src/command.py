from enum import Enum
import subprocess
import sys
import os
import re

class Command:
    """
    Base class representing a shell command.
    All custom commands should inherit from this.
    """
    def __init__(self, name, args, flag_dict=None):
        self._name = name               # Command name (e.g. 'wc', 'cat')
        self._args = args               # Command arguments as list
        self._flag_dict = flag_dict     # Optional dictionary of flags

    def run(self, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
        """
        Method to be overridden by subclasses to implement command behavior.
        """
        pass

    def get_args(self):
        return self._args


class Wc(Command):
    """
    Implementation of the 'wc' command: counts lines, words, and bytes.
    """
    def __init__(self, args, flag_dict=None):
        super().__init__('wc', args, flag_dict)

    def run(self, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
        filenames = self._args
        if filenames:
            for filename in filenames:
                try:
                    with open(filename, "r") as file:
                        content = file.read()
                        lines = content.count('\n')                     # Count newlines
                        words = len(content.split())                    # Count words
                        bytes_size = len(content.encode("utf-8"))       # Count bytes
                        print(f"{lines} {words} {bytes_size} {filename}", file=stdout)
                except FileNotFoundError:
                    print(f"wc: {filename}: No such file or directory", file=stderr)
                    return 1
        else:
            # If no file is provided, read from stdin
            content = stdin.read()
            lines = content.count('\n')
            words = len(content.split())
            bytes_size = len(content.encode("utf-8"))
            print(f"{lines} {words} {bytes_size}", file=stdout)
        return 0


class Cat(Command):
    """
    Implementation of the 'cat' command: prints file contents or stdin.
    """
    def __init__(self, args, flag_dict=None):
        super().__init__('cat', args, flag_dict)
    
    def run(self, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
        filenames = self._args
        if filenames:
            for filename in filenames:
                try:
                    with open(filename, "r") as file:
                        # Output the entire content of the file
                        print(file.read(), end="", file=stdout)
                except FileNotFoundError:
                    print(f"cat: {filename}: No such file or directory", file=stderr)
                    return 1
        else:
            # If no files are provided, read from stdin
            print(stdin.read(), end="", file=stdout)
        return 0


class Echo(Command):
    """
    Implementation of the 'echo' command: prints arguments separated by space.
    """
    def __init__(self, args, flag_dict=None):
        super().__init__('echo', args, flag_dict)
    
    def run(self, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
        print(" ".join(self._args), file=stdout)
        return 0


class Pwd(Command):
    """
    Implementation of the 'pwd' command: prints the current working directory.
    """
    def __init__(self, args, flag_dict=None):
        super().__init__(args, flag_dict)
    
    def run(self, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
        print(os.getcwd(), file=stdout)
        return 0


class Exit(Command):
    """
    Implementation of the 'exit' command: terminates the program.
    """
    def __init__(self, args, flag_dict=None):
        super().__init__('exit', args, flag_dict)
    
    def run(self, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
        # the presence of an extra argument does not affect anything.
        return exit(0)


class External(Command):
    """
    Wraps an external (non-built-in) command using subprocess.
    """
    def __init__(self, args):
        super().__init__(name=args[0], args=args)

    def run(self, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
        try:
            proc = subprocess.Popen(
                self._args,        # Command and arguments
                stdin=stdin,
                stdout=stdout,
                stderr=stderr
            )
            proc.wait()            # Wait for the process to complete
            return proc.returncode
        except FileNotFoundError:
            print("Program name is unknown", file=stderr)
            return 1


class Grep(Command):
    """
    Implementation of the 'grep' command: searches for a pattern in a file.
    Supports flags:
      - ignore_case: case-insensitive matching
      - after: number of lines to show after a match
      - word: match whole words only
    """
    def __init__(self, args, flag_dict=None):
        super().__init__('grep', args, flag_dict)

    def run(self, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
        regex_pattern = self._args[0]
        filename = self._args[1]
        flag_i = self._flag_dict.get("ignore_case")
        flag_A = self._flag_dict.get("after") or 0
        flag_w = self._flag_dict.get("word")

        if flag_A < 0:
            print("grep: -A argument can't be negative", file=stderr)
            return 2

        if flag_w:
            # Match whole words only
            regex_pattern = rf"\b{regex_pattern}\b"

        flags = 0
        if flag_i is None:
            flags = re.IGNORECASE
        try:
            pattern = re.compile(regex_pattern, flags=flags)

            if filename is None:
                file = stdin
            else:
                file = open(filename, "r", encoding="utf-8")

            lines = [line.rstrip("\n") for line in file.readlines()]
            found = False
            for i, line in enumerate(lines):
                if pattern.search(line):
                    found = True
                    # Print match and N following lines
                    for j in range(flag_A + 1):
                        if i + j >= len(lines):
                            break
                        print(lines[i + j], file=stdout)
                    print(25 * "-", file=stdout)  # Separator
            if filename is not None:
                file.close()
        except FileNotFoundError:
            print("grep: file not found", file=stderr)
            return 2

        return 0 if found else 1


class CommandFactory:
    """
    Factory class for creating command instances.
    Maps command names to their respective classes.
    """
    commands = {
        "WC": Wc,
        "CAT": Cat,
        "EXIT": Exit,
        "PWD": Pwd,
        "ECHO": Echo,
        "GREP": Grep
    }

    @classmethod
    def is_enum_value(cls, value):
        """
        Checks if a given command name is a recognized built-in command.
        """
        return value in cls.commands

    @staticmethod
    def build_external(args):
        """
        Returns an External command wrapper (e.g., for system utilities).
        """
        return External(args)

    @classmethod
    def build_command(cls, name, args, flag_dict=None):
        """
        Instantiates a command by name using the corresponding class.
        """
        return cls.commands[name](args=args, flag_dict=flag_dict)
