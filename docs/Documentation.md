# CLI

The system contains the following classes: 
1) Parser - a class, which is in charge of parsing an user input with different settings and getting forms Command further on pipeline
2) ProcessManager - a class, which is responsible for creating new Executor and giving it a new Command
3) Executor - a class, which executes a subprocess for external commands or just python implementation for internal supported commands (wc, cat etc)
4) Command - a class, which encapsulates all logic of Bash command. Usually it's an array of strings.
5) Environment - a class, which stores and gets env variables set during the script run



## Implementation details: 
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
