from src.executor import Executor


class ProcessManager:
    """
    a class, which is responsible for creating new Executor and giving it a new Command
    """
    def __init__(self, environment):
        """
        initializes the ProcessManager with an environment and creates an Executor instance

        :param environment: An instance of the Environment class to manage environment variables
        """
        self.environment = environment
        self.executor = Executor(environment)

    def run_command(self, command):
        """
        executes a command
        if the command is an environment variable assignment,
        it updates the environment. Otherwise, it delegates the execution to the Executor

        :param command: the command to be executed or processed
        """
        if "=" in command.args[0]:  # check for variable assignment
            key, value = command.args[0].split("=", 1)
            self.environment.set_variable(key, value)
        else:
            self.executor.execute(command)
