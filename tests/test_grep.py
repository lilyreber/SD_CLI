import sys
import io
from src.environment import Environment
from src.parser import Parser
from src.pipeline import Pipeline
import pytest


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

def test_parse_grep_ignore_case():
    write_test_file()
    env = Environment()
    command = Parser.parse('grep -i "Minimal" test.txt', env)[0]
    assert command._flag_dict["ignore_case"]

def test_parse_grep_whole_word():
    write_test_file()
    env = Environment()
    command = Parser.parse('grep -w "Минимал" test.txt', env)[0]
    assert command._flag_dict["word"]

def test_parse_grep_after_flag():
    write_test_file()
    env = Environment()
    command = Parser.parse('grep -A 1 "II" test.txt', env)[0]
    assert command._flag_dict["after"] == 1

def test_grep_match_output():
    write_test_file()
    env = Environment()
    command = Parser.parse('grep "Minimal" test.txt', env)[0]
    with open("res", "w+") as res:
        ret = command.run(stdout=res)
        res.seek(0)
        output = res.read()
        assert "Minimal syntax grep" in output
        assert ret == 0

def test_grep_after_flag_output():
    write_test_file()
    env = Environment()
    command = Parser.parse('grep -A 1 "II" test.txt', env)[0]
    with open("res", "w+") as res:
        ret = command.run(stdout=res)
        res.seek(0)
        output = res.read().strip().split("\n")
        assert output[0] == "II testing stage"
        assert output[1] == "next line"
        assert ret == 0

def test_grep_invalid_missing_file():
    env = Environment()
    command = Parser.parse("grep pattern missing.txt", env)[0]
    stderr = io.StringIO()
    ret = command.run(stderr=stderr)
    stderr.seek(0)
    assert "file not found" in stderr.read().lower()
    assert ret != 0
