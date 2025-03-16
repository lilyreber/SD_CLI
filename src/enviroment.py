import os


class Environment:
    def __init__(self):
        self.variables = os.environ.copy()

    def set_variable(self, key, value):
        self.variables[key] = value

    def get_variable(self, key):
        return self.variables.get(key, "")
