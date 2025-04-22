import os
import subprocess
from src.command import Echo, Pwd, Cat, Wc, External


def test_execute_echo():
    """Проверка работы echo"""
    command = Echo(args=["test output"])
    with open("res", 'w+') as res:
        ret = command.run(stdout=res)
        res.seek(0)
        assert res.read().strip() == "test output"
        assert ret == 0

def test_execute_pwd():
    """Проверка работы pwd"""
    command = Pwd(args=[])
    with open("res", "w+") as res:
        ret = command.run(stdout=res)
        res.seek(0)
        assert res.read().strip() == os.getcwd()
        assert ret == 0

def test_execute_cat():
    """Чтение из файла через cat"""
    with open("input.txt", "w") as f:
        f.write("hello\nworld")
    command = Cat(args=["input.txt"])
    with open("res", "w+") as res:
        ret = command.run(stdout=res)
        res.seek(0)
        assert res.read() == "hello\nworld"
        assert ret == 0

def test_execute_wc():
    """Подсчет строк, слов и байт с помощью wc"""
    content = "one two three\nfour five\nsix\n"
    with open("input.txt", "w") as f:
        f.write(content)
    command = Wc(args=["input.txt"])
    with open("res", "w+") as res:
        ret = command.run(stdout=res)
        res.seek(0)
        output = res.read().strip()
        parts = list(map(int, output.split()[:-1]))
        assert output.split()[-1] == 'input.txt'
        assert len(parts) == 3
        assert parts[0] == 3  # строки
        assert parts[1] == 6  # слова
        assert parts[2] == len(content)  # байты
        assert ret == 0

def test_execute_ls():
    """Вывод содержимого директории через ls"""
    os.makedirs("testdir", exist_ok=True)
    with open("testdir/file.txt", "w") as f:
        f.write("data")
    command = External(args=["ls", "testdir"])
    with open("res", "w+") as res:
        ret = command.run(stdin=subprocess.DEVNULL, stdout=res)
        res.seek(0)
        assert "file.txt" in res.read()
        assert ret == 0
