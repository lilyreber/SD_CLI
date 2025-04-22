import pytest
from src.environment import Environment
from src.parser import Parser

def test_substitute_simple():
    """Подстановка переменной $TEST"""
    env = Environment()
    env.set_variable("TEST", "value")
    substituted = env.substitute_vars("echo $TEST")
    cmd = Parser.parse(substituted, env)[0]
    assert cmd._args == ["value"]

def test_substitute_braces():
    """Подстановка переменной ${TEST}"""
    env = Environment()
    env.set_variable("TEST", "value")
    substituted = env.substitute_vars("echo ${TEST}")
    cmd = Parser.parse(substituted, env)[0]
    assert cmd._args == ["value"]

def test_substitute_unknown():
    """Неизвестная переменная не подставляется"""
    env = Environment()
    substituted = env.substitute_vars("echo $UNKNOWN")
    cmd = Parser.parse(substituted, env)[0]
    assert cmd._args == []

def test_substitute_multiple():
    """Подстановка нескольких переменных"""
    env = Environment()
    env.set_variable("VAR1", "hello")
    env.set_variable("VAR2", "world")
    substituted = env.substitute_vars("echo $VAR1 $VAR2")
    cmd = Parser.parse(substituted, env)[0]
    assert cmd._args == ["hello", "world"]

def test_substitute_middle():
    """Подстановка переменной в середине пути"""
    env = Environment()
    env.set_variable("DIR", "docs")
    substituted = env.substitute_vars("ls -l $DIR/files")
    cmd = Parser.parse(substituted, env)[0]
    assert cmd._args == ["ls", "-l", "docs/files"]