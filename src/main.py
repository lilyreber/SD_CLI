from src.enviroment import Environment
from src.parser import Parser
from src.process_manager import ProcessManager


def main():
    """
    it initializes the environment, process manager, and enters a loop to process user input
    """
    env = Environment()
    process_manager = ProcessManager(env)

    while True:
        try:
            input_line = input("cli> ")
            command = Parser.parse(input_line)
            process_manager.run_command(command)
        except KeyboardInterrupt:
            # Handle Ctrl+C interruption gracefully
            print("\nUse 'exit' to quit.")
        except EOFError:
            # Handle Ctrl+D (end-of-file) to exit the program
            print("\nExiting.")
            break

if __name__ == "__main__":
    main()

