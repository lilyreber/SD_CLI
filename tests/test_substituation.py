from src.environment import Environment
from src.parser import Parser


def test_substitute_simple():
    """Проверка подстановки переменной в формате $VAR"""
    env = Environment()
    env.set_variable("TEST", "value")
    line = env.substitute_vars("echo $TEST")
    command = Parser.parse(line, env)[0]
    assert command._args == ["value"]

def test_substitute_with_braces():
    """Проверка подстановки переменной в формате ${VAR}"""
    env = Environment()
    env.set_variable("VAR", "hello")
    line = env.substitute_vars("echo ${VAR}")
    command = Parser.parse(line, env)[0]
    assert command._args == ["hello"]

def test_substitute_multiple_variables():
    """Несколько переменных подряд"""
    env = Environment()
    env.set_variable("A", "1")
    env.set_variable("B", "2")
    line = env.substitute_vars("echo $A $B")
    command = Parser.parse(line, env)[0]
    assert command._args == ["1", "2"]

def test_substitute_missing_variable():
    """Подстановка отсутствующей переменной"""
    env = Environment()
    line = env.substitute_vars("echo $MISSING")
    command = Parser.parse(line, env)[0]
    assert command._args == []

def test_substitute_inside_path():
    """Подстановка переменной внутри пути"""
    env = Environment()
    env.set_variable("DIR", "docs")
    line = env.substitute_vars("ls -l $DIR/files")
    command = Parser.parse(line, env)[0]
    assert command._args == ["ls", "-l", "docs/files"]
