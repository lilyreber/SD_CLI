import os
import re


class Environment:
    """
    a class, which stores and gets env variables set during the script run
    """
    def __init__(self):
        self.__variables = os.environ.copy()

    def set_variable(self, key, value):
        """
        sets the value of the environment variable

        :param key: the name of the variable
        :param value: the value of the variable
        """
        self.__variables[key] = value

    def get_variable(self, key):
        """
        returns the value of the environment variable by key
        if the variable is not found, it returns an empty string

        :param key: the name of the variable
        :return: the value of the variable or an empty string if the variable is not found
        """
        return self.__variables.get(key, "")


    def substitute_vars(self, command_str: str) -> str:
        """
        substitute environment variables in a string

        :param command_str: command
        :return: string with substitute or original if not found
        """

        def replace_match(match):
            var_name = match.group(1) if match.group(1) is not None else match.group(2)
            return self.__variables.get(var_name, "")

        return re.sub(
            r'\$([A-Za-z_][A-Za-z0-9_]*)|\$\{([A-Za-z_][A-Za-z0-9_]*)\}',
            replace_match,
            command_str
        )