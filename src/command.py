from enum import Enum
import subprocess
import sys
import os
import re


class Command:
    """
    a class, which encapsulates all logic of Bash command
    """
    def __init__(self, name, args, flag_dict=None):
        # list of command arguments
        self._name = name
        self._args = args
        self._flag_dict = flag_dict
    
    def run(self, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
        pass

    def get_args(self):
        return self._args


class Wc(Command):

    def __init__(self, args, flag_dict=None):
        super().__init__('wc', args, flag_dict)

    def run(self, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
        filenames = self._args
        if filenames:
            for filename in filenames:
                try:
                    with open(filename, "r") as file:
                        # full text
                        content = file.read()
                        #wc actually counts '\n' too
                        lines = content.count('\n')
                        # split deletes all space symbols and returns an array of words
                        words = len(content.split())
                        # choose encoding then count bytes with len
                        bytes_size = len(content.encode("utf-8"))
                        print(f"{lines} {words} {bytes_size} {filename}", file=stdout)
                except FileNotFoundError:
                    print(f"wc: {filename}: No such file or directory", file=stderr)
                    return 1
        else:
            # read from pipe or stdin
            content = stdin.read()
            #wc actually counts '\n' too
            lines = content.count('\n')
            # split deletes all space symbols and returns an array of words
            words = len(content.split())
            # choose encoding then count bytes with len
            bytes_size = len(content.encode("utf-8"))
            print(f"{lines} {words} {bytes_size}", file=stdout)
        return 0

class Cat(Command):
    def __init__(self, args, flag_dict=None):
        super().__init__('cat', args, flag_dict)
    
    def run(self, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
        filenames = self._args
        if filenames:
            for filename in filenames:
                try:
                    with open(filename, "r") as file:
                        #full text of file
                        print(file.read(), end="", file=stdout)
                except FileNotFoundError:
                    print(f"cat: {filename}: No such file or directory", file=stderr)
                    return 1
        else:
            print(stdin.read(), end="", file=stdout)
        return 0

class Echo(Command):
    def __init__(self, args, flag_dict=None):
        super().__init__('echo', args, flag_dict)
    
    def run(self,stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
        print(" ".join(self._args), file=stdout)
        return 0

class Pwd(Command):
    def __init__(self, args, flag_dict=None):
        super().__init__(args, flag_dict)
    
    def run(self, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
        print(os.getcwd(), file=stdout)
        return 0

class Exit(Command):
    def __init__(self, args, flag_dict=None):
        super().__init__('exit', args, flag_dict)
    
    def run(self, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
        return exit(0)
    
class External(Command):
    def __init__(self, args):
        super().__init__(name=args[0], args=args)

    def run(self, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
        try:
            proc = subprocess.Popen(
            self._args,
            stdin=stdin,
            stdout=stdout,
            stderr=stderr
            )
            proc.wait()
            return proc.returncode
        except FileNotFoundError:
            print("Program name is unknown", file=stderr)
            return 1

class Grep(Command):
    def __init__(self, args, flag_dict=None):
        super().__init__('grep', args, flag_dict)

    def run(self, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
        regex_pattern, filename = self._args[0], self._args[1]
        flag_i = self._flag_dict.get("ignore_case")
        flag_A = self._flag_dict.get("after") or 0
        flag_w = self._flag_dict.get("word")

        if flag_w:
            regex_pattern = rf"\b{regex_pattern}\b"

        flags = 0

        if flag_i != None:
            flags = re.IGNORECASE

        pattern = re.compile(regex_pattern, flags=flags)

        with open(filename, "r", encoding="utf-8") as file:
            lines = [line.rstrip("\n") for line in file.readlines()]
            found = False
            for i, line in enumerate(lines):
                if pattern.search(line):
                    found = True
                    for j in range(flag_A + 1):
                        if i + j >= len(lines):
                            break
                        print(lines[i + j], file=stdout)
                    print(25*"-", file=stdout)
        if found:
            return 0
        return 1


class CommandFactory:
    commands = {
        "WC":Wc,
        "CAT":Cat,
        "EXIT":Exit,
        "PWD":Pwd,
        "ECHO":Echo,
        "GREP": Grep
        }
    

    @classmethod
    def is_enum_value(cls, value):
        return value in cls.commands
    
    @staticmethod
    def build_external(args):
        return External(args)
    
    @classmethod
    def build_command(cls, name, args, flag_dict=None):
        return cls.commands[name](args=args, flag_dict=flag_dict)