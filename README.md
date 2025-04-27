# ShellLibrary
-------------

A simple Python shell library that allows users to create and extend a customizable shell interface. 
This library supports basic commands like `exit`, `clear`, `gset`, `gget`, `gsets`, and `help`, as well as the ability to add custom commands and extend functionality.

## Default Commands/Features
---------

- `exit`: Exit the shell.
- `clear`: Clear the terminal screen.
- `gset <key> <value>`: Set a global environment variable.
- `gget <key>`: Get the value of a global environment variable.
- `gsets`: Display all global environment variables in a clean format.
- `help`: Displays help information for commands.

## How to Use
-----------

1. Clone the repository or copy the code into your project.

2. Import the `Shell` class into your Python code:

      ```python
      from shelllib import Shell
      ```

3. Create an instance of the `Shell` class and run the shell:

      ```python
      shell = Shell()
      shell.run_shell()
      ```

4. To customize the shell's prompt, add custom commands, or modify its behavior, you can create and pass your own set of commands:

      ```python
      def custom_command(arguments, shell_instance):
          shell_instance.prompt = "newprompt> " 
          print(f"Custom command executed with arguments: {arguments}")

      custom_commands = {
          "mycommand": {
              "function": custom_command,
              "help": "This is a custom command"
          }
      }

      shell.set_commands(custom_commands)
      shell.run_shell()
      ```

5. Use `help` to get help for commands:

      ```python
      help
      ```

## Command Customization
----------------------

You can customize commands by passing a dictionary of custom commands to the `Shell` instance. Each custom command should have a name, a function, and an optional help message:

      ```python
      def custom_function(arguments, shell_instance):
          shell_instance.prompt = "newprompt> " 
          print(f"Custom function executed with arguments: {arguments}")

      custom_commands = {
          "customcmd": {
              "function": custom_function,
              "help": "This is a custom command"
          }
      }
      ```
