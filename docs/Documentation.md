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
  * get list of commands 




## Implementation details: 
 that reads user input, gives input to the parser, and then a parsed string for execution in the Pipeline.
a class, which is in charge of parsing an user input with different settings and getting forms Command further on pipeline
1) After processing a command, the Main function checks whether the command includes assigning environment variables. If so, we invoke the setter by Environment class.
2) Object of Executor class is logical process which is responsible only for running its own Command
3) No parallelism is needed. If two commands are called in a line they are anyway connected via pipe and the next command can’t be called before the previous because it depends on its output.
4) Parser uses shlex parser which is specified for parsing shell-like strings. 
5) Executor uses subprocess from subprocess package.
	


## Pipeline:
* Parser parses commands and creates a Command object, gives it to a process manager or sets an env variable calling for Environment class
* Else, if it’s a command, Process manager creates Executor and gives it the Command and substitutes env variables. Process manager reassigns stdin stdout if a pipe is needed.
* Executor defines command type and either uses our implementation for internal commands or calls subprocess. If anything raises we rethrow an error up to the Main. 
* Chain of commands separated by pipes are treated as one logical command given to bash. Hence, at the end of execution the chain the Main execution sets the status code of this logical command.
