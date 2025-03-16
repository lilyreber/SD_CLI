import subprocess
import os

class Executor:
    """Class executor stores env variables and executes commands depending on their name
    To construct it you only need an Environment class instance"""
    def __init__(self, environment):
        # Environment class here
        self.environment = environment
    
    def execute(self, command):
        if not command.args:
            return
        
        # read name of the command
        cmd = command.args[0]
    
        if cmd == "echo":
            print(" ".join(command.args[1:]))
        elif cmd == "pwd":
            print(os.getcwd())
        elif cmd == "cat":
            self._cat(command.args[1:])
        elif cmd == "wc":
            self._wc(command.args[1:])
        elif cmd == "exit":
            exit(0)
        else:
            # command unknown so we try to run_external
            self._run_external(command)
    
    def _cat(self, filenames):
        for filename in filenames:
            try:
                with open(filename, "r") as file:
                    #full text of file
                    print(file.read(), end="")
            except FileNotFoundError:
                print(f"cat: {filename}: No such file or directory", file=os.sys.stderr)
    
    def _wc(self, filenames):
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
                    print(f"{lines} {words} {bytes_size} {filename}")
            except FileNotFoundError:
                print(f"wc: {filename}: No such file or directory", file=os.sys.stderr)
    
    def _run_external(self, command):
        try:
            # instead of exec in C
            subprocess.run(command.args, env=self.environment.variables)
        except FileNotFoundError:
            print(f"{command.args[0]}: command not found", file=os.sys.stderr)