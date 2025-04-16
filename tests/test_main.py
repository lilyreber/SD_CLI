import os

from src.command import *
from src.environment import Environment
from src.pipeline import Pipeline
from src.parser import Parser
import pytest
import io


def test_substitute_simple():
    env = Environment()
    env.set_variable("TEST", "value")
    input_line = "echo $TEST"
    substituted_line = env.substitute_vars(input_line)
    commands = Parser.parse(substituted_line, env)
    assert len(commands) == 1
    command = commands[0]

    assert str(type(command)) == "<class 'command.Echo'>"
    assert command._args == ['value']


def test_substitute_braces():
    env = Environment()
    env.set_variable("TEST", "value")
    input_line = "echo ${TEST}"
    substituted_line = env.substitute_vars(input_line)
    commands = Parser.parse(substituted_line, env)
    assert len(commands) == 1
    command = commands[0]

    assert str(type(command)) == "<class 'command.Echo'>"
    assert command._args == ['value']


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
    assert command._args == ['hello', 'world']


def test_substitute_unknown():
    env = Environment()
    input_line = "echo $UNKNOWN"
    substituted_line = env.substitute_vars(input_line)
    commands = Parser.parse(substituted_line, env)
    assert len(commands) == 1
    command = commands[0]

    assert str(type(command)) == "<class 'command.Echo'>"
    assert command._args == []


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
    assert command._args == ['ls', '-l', 'docs/files']


# def test_substitute_system():
#     env = Environment()
#     input_line = "echo $HOME"
#     substituted_line = env.substitute_vars(input_line)
#     commands = Parser.parse(substituted_line, env)
#     assert len(commands) == 1
#     command = commands[0]

#     assert str(type(command)) == "<class 'command.Echo'>"
#     assert command._args == [os.getenv("HOME")]



def test_execute_echo():
    command = Echo(args=["test output"])
    res = open("res", 'w+')
    ret = command.run(stdout=res)
    res.seek(0)
    assert res.read().strip() == "test output"
    assert ret == 0
    # os.remove("res")

def test_execute_pwd():
    import os
    command = Pwd(args=['amogus'])
    res = open("res", "w+")
    ret = command.run(stdout=res)
    res.seek(0)
    assert res.read().strip() == os.getcwd()
    assert ret == 0

def test_execute_cat():
    with open("input.txt", "w") as f:
        f.write("hello\nworld")

    command = Cat(args=["input.txt"])
    res = open("res", "w+")
    ret = command.run(stdout=res)
    res.seek(0)
    assert res.read() == "hello\nworld"
    assert ret == 0

def test_execute_wc():
    content = "one two three\nfour five\nsix\n"
    with open("input.txt", "w") as f:
        f.write(content)

    command = Wc(args=["input.txt"])
    res = open("res", "w+")
    ret = command.run(stdout=res)
    res.seek(0)
    output = res.read().strip()
    parts = list(map(int, output.split()[:-1]))
    
    assert output.split()[-1] == 'input.txt'
    assert len(parts) == 3
    assert parts[0] == 3  # lines
    assert parts[1] == 6  # words
    assert parts[2] == len(content)  # bytes
    assert ret == 0

def test_execute_ls():
    os.makedirs("testdir", exist_ok=True)
    with open("testdir/file.txt", "w") as f:
        f.write("data")

    command = External(args=["ls", "testdir"])
    res = open("res", "w+")
    ret = command.run(stdin=subprocess.DEVNULL,stdout=res)
    res.seek(0)
    assert "file.txt" in res.read()
    assert ret == 0

    # os.remove("testdir/file.txt")
    # os.rmdir("testdir")

def test_parse_simple_echo():
    env = Environment()
    command = Parser.parse("echo hello world", env)[0]
    assert command._name == 'echo'
    assert command._args == ["hello", "world"]

def write_test_file():
    with open("test.txt", "w", encoding="utf-8") as f:
        f.write("Minimal syntax grep\n")
        f.write("II testing stage\n")
        f.write("next line\n")

def test_parse_grep_exact_match():
    write_test_file()
    env = Environment()
    command = Parser.parse('grep "Minimal" test.txt', env)[0]
    assert command._args == ["Minimal", "test.txt"]
    assert command._flag_dict == {'word': False, 'ignore_case': False, 'after': None}


def test_parse_grep_dollar_anchor():
    write_test_file()
    env = Environment()
    command = Parser.parse('grep "Minimal$" test.txt', env)[0]
    assert command._args == ["Minimal$", "test.txt"]
    assert command._flag_dict == {'word': False, 'ignore_case': False, 'after': None}


def test_parse_grep_caret_anchor():
    write_test_file()
    env = Environment()
    command = Parser.parse('grep "^Minimal" test.txt', env)[0]
    assert command._args == ["^Minimal", "test.txt"]
    print (command._flag_dict)
    assert command._flag_dict == {'word': False, 'ignore_case': False, 'after': None}


def test_parse_grep_ignore_case():
    write_test_file()
    env = Environment()
    command = Parser.parse('grep -i "Minimal" test.txt', env)[0]
    assert command._args == ["Minimal", "test.txt"]
    assert command._flag_dict["ignore_case"] is True


def test_parse_grep_whole_word():
    write_test_file()
    env = Environment()
    command = Parser.parse('grep -w "Минимал" test.txt', env)[0]
    assert command._args == ["Минимал", "test.txt"]
    assert command._flag_dict["word"] is True


def test_parse_grep_after_flag():
    write_test_file()
    env = Environment()
    command = Parser.parse('grep -A 1 "II" test.txt', env)[0]
    assert command._args == ["II", "test.txt"]
    assert command._flag_dict["after"] == 1

def test_grep_match_output():
    env = Environment()
    command = Parser.parse('grep "Minimal" test.txt', env)[0]
    res = open("res", "w+")
    ret = command.run(stdout=res)
    res.seek(0)
    output = res.read()
    assert "Minimal syntax grep" in output
    assert ret == 0


def test_grep_no_match_output():
    env = Environment()
    command = Parser.parse('grep "Minimal$" test.txt', env)[0]
    res = open("res", "w+")
    ret = command.run(stdout=res)
    res.seek(0)
    output = res.read()
    assert output.strip() == ""
    assert ret == 1  # grep returns 1 if no matches


def test_grep_ignore_case_output():
    env = Environment()
    command = Parser.parse('grep -i "Minimal" test.txt', env)[0]
    res = open("res", "w+")
    ret = command.run(stdout=res)
    res.seek(0)
    output = res.read()
    assert "Minimal syntax grep" in output
    assert ret == 0


def test_grep_after_flag_output():
    env = Environment()
    command = Parser.parse('grep -A 1 "II" test.txt', env)[0]
    res = open("res", "w+")
    ret = command.run(stdout=res)
    res.seek(0)
    output = res.read()
    lines = output.strip().split("\n")
    assert lines[0] == "II testing stage"
    assert lines[1] == "next line"
    assert ret == 0

def test_unknown():
    env = Environment()
    command = Parser.parse('foo bar baz', env)[0]
    res = open("res", "w+")
    ret = command.run(stdin=subprocess.DEVNULL,stderr=res)
    res.seek(0)
    output = res.read()
    assert output == "Program name is unknown\n"

def test_grep_basic_file():
    with open("build.gradle", "w") as f:
        f.write("apply plugin: 'java'\n")
        f.write("version = '1.0'\n")

    env = Environment()
    command = Parser.parse('grep plugin build.gradle', env)[0]
    res = open("res", "w+")
    ret = command.run(stdout=res)
    res.seek(0)
    output = res.read()
    assert "plugin" in output
    assert ret == 0

def test_grep_basic_pipe():
    with open("build.gradle", "w") as f:
        f.write("apply plugin: 'java'\n")
        f.write("version = '1.0'\n")

    command = Parser.parse("cat build.gradle | grep plugin", Environment())
    res = open("res", "w+")
    sys.stdout = res
    ret = Pipeline().execute(command)
    res.seek(0)
    assert "plugin" in res.read()
    sys.stdout = sys.__stdout__

def test_grep_regex():
    with open("build.gradle", "w") as f:
        f.write("apply plugin: 'java'\n")
        f.write("apply plulin: 'kotlin'\n")

    env = Environment()
    command = Parser.parse('grep p.u.*n build.gradle', env)[0]
    res = open("res", "w+")
    sys.stdout = res
    command.run(stdout=res)
    res.seek(0)
    output = res.read()
    assert "plugin" in output
    assert "plulin" in output


def run_with_stderr(cmdline: str):
    env = Environment()
    command = Parser.parse(cmdline, env)[0]
    stderr = io.StringIO()
    ret = command.run(stderr=stderr)
    stderr.seek(0)
    return ret, stderr.read()

def test_grep_invalid_A_missing_argument():
    try:
        env = Environment()
        file = open("err", "w+")
        sys.stderr = file
        command = Parser.parse("grep -A plugin build.gradle", env)[0]
    except IndexError:
        file.seek(0)
        assert "invalid int" in file.read()
        file.close()
    finally:
        sys.stderr = sys.__stderr__ 
        # os.remove("err")

def test_grep_invalid_negative_after():
    ret, err = run_with_stderr("grep -A -1 plugin build.gradle")
    assert ret != 0
    assert "error" in err.lower() or err.strip() != ""

def test_grep_invalid_missing_file():
    ret, err = run_with_stderr("grep plugin ololo")
    assert ret != 0
    assert "file not found" in err

def test_cat_grep_wc_chain():
    with open("data.txt", "w") as f:
        f.write("apple\nbanana\napple pie\norange\n")

    env = Environment()
    out = open("out", 'w+')
    sys.stdout = out
    command = Parser.parse("cat data.txt | grep -i 'apple' | wc ", env)
    ret = Pipeline().execute(command)
    out.seek(0)
    output = out.read()
    words = output.strip().split()
    sys.stdout = sys.__stdout__
    # os.remove("data.txt")
    # os.remove("out")
    assert int(words[0]) == 4
    