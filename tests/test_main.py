import os

from src.command import Command
from src.environment import Environment
from src.executor import Executor
from src.parser import Parser
from src.process_manager import ProcessManager


def test_parse_simple_command():
    command = Parser.parse("echo hello world")
    assert command.args == ["echo", "hello", "world"]

def test_set_environment_variable():
    env = Environment()
    env.set_variable("TEST_VAR", "123")
    assert env.get_variable("TEST_VAR") == "123"

def test_execute_echo(capsys):
    env = Environment()
    executor = Executor(env)
    command = Command(["echo", "test output"])
    executor.execute(command)
    captured = capsys.readouterr()
    assert captured.out.strip() == "test output"

def test_execute_pwd(capsys):
    env = Environment()
    executor = Executor(env)
    command = Command(["pwd"])
    executor.execute(command)
    captured = capsys.readouterr()
    assert captured.out.strip() == os.getcwd()

def test_execute_invalid_command(capsys):
    env = Environment()
    executor = Executor(env)
    command = Command(["non_existent_command"])
    executor.execute(command)
    captured = capsys.readouterr()
    assert "command not found" in captured.err.strip()

def test_execute_variable_assignment():
    env = Environment()
    process_manager = ProcessManager(env)
    command = Command(["MYVAR=hello"])
    process_manager.run_command(command)
    assert env.get_variable("MYVAR") == "hello"

def test_execute_simple_pipe(capsys):
    env = Environment()
    process_manager = ProcessManager(env)
    command = Command(["echo hello | wc -w"])
    process_manager.run_command(command)
    captured = capsys.readouterr()
    assert captured.out.strip() == ""

def test_execute_multi_pipe(capsys):
    env = Environment()
    process_manager = ProcessManager(env)
    command = Command(["echo one two three | tr ' ' '\n' | wc -l"])
    process_manager.run_command(command)
    captured = capsys.readouterr()
    assert captured.out.strip() == ""

def test_execute_invalid_pipe_command(capsys):
    env = Environment()
    process_manager = ProcessManager(env)
    command = Command(["echo test | non_existent_command"])
    process_manager.run_command(command)
    captured = capsys.readouterr()
    assert "command not found" in captured.err.strip()