# CLI

## Components
The system contains the following classes and interfaces: 
* `CLI` - implements a command-line interface
  * reads user input
  * gives input to the `Parser`
  * gives a parsed string for execution in the `Pipeline`.
* `Parser` - parse input string
  * split input string
  * substitutes environment variables
  * divides input by pipes
* `Command` - interface for command for CLI
   * Classes that implements these interface
      * `Wc` - counts lines, words, and bytes in a file 
      * `Cat` - outputs file contents 
      * `Echo` - prints arguments
      * `Pwd` - prints the current directory
      * `Exit` - terminates the CLI 
      * `Grep` - searches for regex patterns. Supports flags: -i (ignore case), -w (whole words), -A N (print N lines after a match).
* `Pipeline` 
  * Redirects I/O streams when using pipelines.
* `Environment`
  * Manages the environment variables while the script is running.
    

    
## Implementation details: 
1) No parallelism is needed. 
2) If two commands are called in a line they are anyway connected via pipe and the next command can’t be called before the previous because it depends on its output.
3) Parser uses argparse library for parsing command line arguments.
4) `External` uses subprocess from subprocess package.
5) We used argparse to parse grep which makes the architecture worse, but any common parser will fail since it should know what flags require args and what do not, which implies that parser actually knows about commands...
6) grep parsing uses argparse because it is impossible to make a common parser that knows which flags need arguments and which do not. It breaks the architecture in this place, gives abstraction leak but fixing it now would take much effort.


## Pipeline:
1) Main initializes and launches the `CLI`
 2) The CLI runs an endless loop that reads input from the terminal. 
 3) `CLI` calls `Parse.run` for input data. 
 4) 'Parse', calling `Environment.substitute_vars`, performs substitution of environment variables. 
 5) We make a split by '|'
 6) For each part, we determine whether the user initializes an environment variable or asks to execute a command. 
 7) If this is a new variable, then we will add it to the `Environment`
 8) If this is a command, then referring to the `CommandFactory` we get an object of the class `Command` corresponding to the successor command
 9) After receiving the list of `Command` heirs, the `CLI` starts executing these commands using `pipeline.execute`
 10) `Pipline` redirects input and output streams and asks the successor of `Command` to perform the corresponding action by calling `Command.run`
 11) If a subcommand in Pipline fails, the error code and the error message are sent to the CLI, to the output stream.