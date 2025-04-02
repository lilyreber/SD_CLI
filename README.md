# SD_CLI
[![Tests](https://github.com/lilyreber/SD_CLI/actions/workflows/python-app.yml/badge.svg)](https://github.com/lilyreber/SD_CLI/actions/workflows/python-app.yml/badge.svg)
![GitHub License](https://img.shields.io/github/license/lilyreber/SD_CLI)


The system is a command interpreter (CLI) designed to process user input, execute commands, and manage the environment. 
The interpreter must be able to work with pipelines (the “|” operator), environment variables, double and single quotes. 
The following commands must be supported:
* cat [FILE] — display the contents of the file
* echo — display your argument (or arguments) on the screen
* wc [FILE] — output the number of lines, words, and bytes in a file
* pwd — print the current directory
* exit — exit the interpreter
* grep is a command—line utility that finds lines matching a given regular expression and outputs them.
* calling an external program via Process (or its analogues), if the entered command is not described above.




# Installation
```bash
git clone https://github.com/lilyreber/SD_CLI
```

# Usage example
```bash
python3 src/main.py
cli> pwd
/home/igor/SD_CLI
cli> echo 123
123
```

# Dependencies
### `argparse`

Parser uses `argparse` library for parsing command line arguments.

* Advantages:
    * Does not require installation of dependencies (pip install is not needed)
    * Without redundant code
    * Compatibility with any version of Python.
* Alternatives:
  * Click 
    * requires installation (pip install click), while argparse is built into Python.
    * сlick uses decorators (@click.command, @click.option), which adds complex code for basic tasks.
  * Typer
    * requires Python 3.6+ and installation (pip install typer).
    * redundancy for simple scripts
  
## Contributors
* [Imamutdinova Liliia](https://github.com/lilyreber)
* [Saprygin Igor](https://github.com/SapryginIgor)
* [Stovba Igor](https://github.com/Igor-Stovba)