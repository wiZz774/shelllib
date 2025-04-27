# Shell Library

A simple Python shell library that allows users to create and extend a customizable shell interface. This library supports basic commands like `exit`, `clear`, and environment variable management (`gset`, `gget`, `gsets`), along with custom user-defined commands.

## Features

- **Interactive Shell**: Create a custom shell with a prompt of your choice.
- **Basic Commands**: Includes commands like `exit`, `clear`, and `help`.
- **Environment Variables**: Supports setting (`gset`), getting (`gget`), and listing (`gsets`) environment variables.
- **Custom Commands**: Easily add custom commands to the shell.
- **Tab Completion**: Provides tab completion for commands and file paths.
  
## Usage

### 1. Clone the Repository

To get started, first clone the repository to your local machine:

```bash
git clone https://github.com/your-username/shelllib.git
cd shelllib
```

2. Using the Shell Class

You can use the Shell class in your own Python projects or interactively via the command line.
Example: Create and Run a Shell

from shelllib import Shell

# Create a new shell instance with a custom prompt
shell = Shell(prompt="MyShell> ")

# Start the shell to begin interacting
shell.run_shell()

This will start the interactive shell with the prompt MyShell>. You can type in commands like exit, clear, help, and others.
3. Default Commands

By default, the shell supports the following commands:

    exit: Exits the shell.

    clear: Clears the terminal screen.

    help: Displays help information about available commands.

    gset <key> <value>: Sets a global environment variable.

    gget <key>: Gets the value of a global environment variable.

    gsets: Displays all global environment variables in a clean, tabular format.

Example of Commands:

    Exit the shell:
    Simply type exit and press Enter.

    Clear the screen:
    Type clear to clear the terminal screen.

    Set an environment variable:
    Use gset to set a global variable, e.g.:

gset MY_VAR "Hello, World!"

Get the value of an environment variable:
Use gget to retrieve the value of a variable, e.g.:

    gget MY_VAR

    List all environment variables:
    Use gsets to see all set environment variables in a table format.

4. Custom Commands

You can easily add your own custom commands to the shell by passing a dictionary of commands to the Shell class. Each command should be a dictionary containing the function to be executed and an optional help message.
Example: Adding a Custom Command

To add a command called scanmode that changes the prompt:

def scanmode_command(arguments, shell_instance):
    shell_instance.set_prompt("scan> ")

def get_commands():
    return {
        "scanmode": {
            "function": scanmode_command,
            "help": "Activate scan mode"
        }
    }

# Create the shell instance with custom commands
shell = Shell(prompt=">>> ", commands=get_commands())

# Run the shell
shell.run_shell()

In this example, the scanmode command changes the shell prompt to scan> . You can add more commands to the get_commands function as needed.
5. Tab Completion

Tab completion is available for both commands and file paths. When you type part of a command or file path and press the Tab key, it will attempt to complete your input.
6. Help Command

To see help for all commands, type help:

help

To get help for a specific command, type help <command_name>:

help gset

This will show the description of the gset command.
7. Exiting the Shell

To exit the shell, you can either type exit or use Ctrl+C.
Installation

If you want to use this library as part of your own project, you can simply copy the shell.py file or clone the entire repository.

Alternatively, you can install it via pip if you prefer (though that's not necessary if you're just copying the code).

pip install git+https://github.com/your-username/shelllib.git

Contributing

Feel free to fork the repository, make changes, and submit pull requests. Any contributions are welcome!
License

This project is licensed under the MIT License - see the LICENSE file for details.
Contact

For questions or suggestions, feel free to open an issue or contact the project owner.
Example Commands Available in the Shell:
Command Name	Help Message
exit	Use exit or Ctrl-C to exit.
clear	Clears the terminal screen.
gset	Sets a global environment variable.
gget	Gets the value of a global environment variable.
gsets	Displays all global environment variables.
help	Displays help information for a command.
