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
        Substitute environment variables in a string, 
        но не трогает строки в одинарных кавычках.

        :param command_str: command
        :return: string with substitution, кроме участков в одинарных кавычках
        """

        pattern = re.compile(r"(\'[^\']*\'|[^']+)")

        def replace_in_segment(segment):
            if segment.startswith("'") and segment.endswith("'"):
                return segment

            return re.sub(
                r'\$([A-Za-z_][A-Za-z0-9_]*)|\$\{([A-Za-z_][A-Za-z0-9_]*)\}',
                lambda match: self.__variables.get(
                    match.group(1) or match.group(2), ""
                ),
                segment
            )

        return ''.join(replace_in_segment(m.group(0)) for m in pattern.finditer(command_str))