import os


class Environment:
    """
    a class, which stores and gets env variables set during the script run
    """
    def __init__(self):
        self.variables = os.environ.copy()

    def set_variable(self, key, value):
        """
        sets the value of the environment variable

         :param key: the name of the variable
         :param value: the value of the variable
        """
        self.variables[key] = value

    def get_variable(self, key):
        """
        returns the value of the environment variable by key
        if the variable is not found, it returns an empty string

        :param key: the name of the variable
        :return: the value of the variable or an empty string if the variable is not found
        """
        return self.variables.get(key, "")
