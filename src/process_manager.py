import subprocess
import os
from src.executor import Executor

class ProcessManager:
    """
    A class responsible for creating new Executor instances and handling command execution,
    including environment variable assignments and pipelines.
    """
    def __init__(self, environment):
        """
        Initializes the ProcessManager with an environment and creates an Executor instance.
        
        :param environment: An instance of the Environment class to manage environment variables.
        """
        self.environment = environment
        self.executor = Executor(environment)

    def run_command(self, command):
        """
        Executes a command. If it's an environment variable assignment, updates the environment.
        If the command includes a pipeline ('|'), processes it accordingly.
        Otherwise, delegates execution to the Executor.

        :param command: The command to be executed or processed.
        """
        if "=" in command.args[0]:  # Check for variable assignment
            key, value = command.args[0].split("=", 1)
            self.environment.set_variable(key, value)
        elif "|" in command.args:  # Check for pipeline
            self._execute_pipeline(command.args)
        else:
            self.executor.execute(command)
    
    def _execute_pipeline(self, commands):
        """
        Executes a series of piped commands by setting up subprocess pipes.
        
        :param commands: List of command arguments split by '|'.
        """
        processes = []
        prev_process = None
        try:
            for cmd in " ".join(commands).split("|"):
                cmd_parts = cmd.strip().split()
                if not cmd_parts:
                    continue
                
                if prev_process is None:
                    process = subprocess.Popen(cmd_parts,
                                                stdin=None,
                                                stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE,
                                                env=self.environment.variables)
                else:
                    process = subprocess.Popen(cmd_parts,
                                            stdin=prev_process.stdout,
                                                stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE,
                                                env=self.environment.variables)
                    prev_process.stdout.close()
                
                prev_process = process
                processes.append(process)
            
            if processes:
                output, error = processes[-1].communicate()
                if output:
                    print(output.decode())
                if error:
                    print(error.decode(), file=os.sys.stderr)
        except:
            print("Not known command")
