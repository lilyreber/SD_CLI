import os

from src.command import *
from src.environment import Environment
from src.parser import Parser


def test_substitute_simple():
    env = Environment()
    env.set_variable("TEST", "value")
    input_line = "echo $TEST"
    substituted_line = env.substitute_vars(input_line)
    commands = Parser.parse(substituted_line, env)
    assert len(commands) == 1
    command = commands[0]

    assert str(type(command)) == "<class 'command.Echo'>"
    assert command.args == ['value']


def test_substitute_braces():
    env = Environment()
    env.set_variable("TEST", "value")
    input_line = "echo ${TEST}"
    substituted_line = env.substitute_vars(input_line)
    commands = Parser.parse(substituted_line, env)
    assert len(commands) == 1
    command = commands[0]

    assert str(type(command)) == "<class 'command.Echo'>"
    assert command.args == ['value']


def test_substitute_multiple():
    env = Environment()
    env.set_variable("VAR1", "hello")
    env.set_variable("VAR2", "world")
    input_line = "echo $VAR1 $VAR2"
    substituted_line = env.substitute_vars(input_line)
    commands = Parser.parse(substituted_line, env)
    assert len(commands) == 1
    command = commands[0]

    assert str(type(command)) == "<class 'command.Echo'>"
    assert command.args == ['hello', 'world']


def test_substitute_unknown():
    env = Environment()
    input_line = "echo $UNKNOWN"
    substituted_line = env.substitute_vars(input_line)
    commands = Parser.parse(substituted_line, env)
    assert len(commands) == 1
    command = commands[0]

    assert str(type(command)) == "<class 'command.Echo'>"
    assert command.args == []


def test_substitute_middle():
    env = Environment()
    env.set_variable("DIR", "docs")
    input_line = "ls -l $DIR/files"
    substituted_line = env.substitute_vars(input_line)
    commands = Parser.parse(substituted_line, env)
    assert len(commands) == 1
    command = commands[0]

    print(commands)
    assert str(type(command)) == "<class 'command.External'>"
    assert command.args == ['ls', '-l', 'docs/files']


def test_substitute_system():
    env = Environment()
    input_line = "echo $HOME"
    substituted_line = env.substitute_vars(input_line)
    commands = Parser.parse(substituted_line, env)
    assert len(commands) == 1
    command = commands[0]

    assert str(type(command)) == "<class 'command.Echo'>"
    assert command.args == [os.getenv("HOME")]