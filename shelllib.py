import readline
import sys
import os
import re


class Shell:
    def __init__(self, prompt='> ', basic_commands=True, commands=None):
        self.prompt = prompt
        self.env_vars = {}
        self.commands = {}
        self.command_help = {}

        # Default Commands Setup
        if commands is None:
            commands = {}

        if basic_commands:
            # Default commands and their descriptions
            self.command_help = {
                "exit": "Use exit or Ctrl-C to exit.",
                "clear": "Clears this Console.",
                "gset": "Sets a global environment variable.",
                "gget": "Gets the value of a global environment variable.",
                "gsets": "Displays all global environment variables in a clean format.",
                "help": "Displays help information for a command."
            }

            # Registering default command functions
            default_commands = {
                "exit": {"function": self.exit, "help": "Use exit or Ctrl-C to exit."},
                "clear": {"function": self.clear, "help": "Clears this Console."},
                "gset": {"function": self.gset, "help": "Sets a global environment variable."},
                "gget": {"function": self.gget, "help": "Gets the value of a global environment variable."},
                "gsets": {"function": self.gsets, "help": "Displays all global environment variables in a clean format."},
                "help": {"function": self.help, "help": "Displays help information for a command."}
            }

            self.commands = default_commands

        # Register user-provided commands
        for cmd_name, cmd_func in commands.items():
            self.commands[cmd_name] = cmd_func["function"]
            self.command_help[cmd_name] = cmd_func.get("help", "No help message.")

    def set_commands(self, commands):
        """Update commands dynamically without clearing existing ones."""
        if not isinstance(commands, dict):
            print("Error: Commands should be passed as a dictionary.")
            return

        # Add new commands and their help messages
        for cmd_name, cmd_func in commands.items():
            self.commands[cmd_name] = cmd_func["function"]
            self.command_help[cmd_name] = cmd_func.get("help", "No help message.")

    def set_prompt(self, new_prompt):
        """Set a custom prompt for the shell."""
        self.prompt = new_prompt

    def run_shell(self):
        """Start the shell and process user input in a loop."""
        try:
            self.setup_readline()
            while True:
                user_input = input(self.prompt)
                user_input_parsed = self.parse_commandline(user_input)

                if not user_input_parsed:
                    continue

                user_input_command = user_input_parsed[0]
                user_input_arguments = user_input_parsed[1:]

                # Check if the command exists
                if user_input_command in self.commands:
                    # If it's a function, call it directly
                    cmd_entry = self.commands[user_input_command]
                    if callable(cmd_entry):
                        cmd_entry(user_input_arguments, self)  # Call function directly
                    else:
                        cmd_entry["function"](user_input_arguments)  # Call the function inside the dictionary
                else:
                    print(f"{user_input_command}: command not found")
        except KeyboardInterrupt:
            print()



    def parse_commandline(self, cmd_line):
        """Parse the command line into arguments."""
        pattern = r'"([^"\\]*(?:\\.[^"\\]*)*)"|\'([^\']*(?:\\.[^\'\\]*)*)\'|(\S+)'

        args = re.findall(pattern, cmd_line)
        flattened_args = []

        for match in args:
            arg = next(filter(None, match))
            arg = re.sub(r'\\(.)', r'\1', arg).strip()

            if (arg.startswith('"') and arg.endswith('"')) or (arg.startswith("'") and arg.endswith("'")):
                arg = arg[1:-1]  # Remove surrounding quotes

            arg = self.expand_variables(arg)
            flattened_args.append(arg)

        return flattened_args

    def setup_readline(self):
        """Set up tab completion for commands and file paths."""
        readline.set_completer(self.command_completer)
        readline.parse_and_bind("tab: complete")

    def command_completer(self, text, state):
        """Custom tab completion for commands and file paths."""
        options = [command for command in self.commands if command.startswith(text)]

        if not options:
            options = self.file_completer(text)

        return options[state] if state < len(options) else None

    def file_completer(self, text):
        """Return a list of file paths that match the input text."""
        if text.endswith('/'):
            text = text[:-1]
            options = [d for d in os.listdir('.') if d.startswith(text) and os.path.isdir(d)]
        else:
            options = [f for f in os.listdir('.') if f.startswith(text) and os.path.isfile(f)]

        return [f + '/' if os.path.isdir(f) else f for f in options]

    def expand_variables(self, text):
        """Expand variables in the format $key to their values."""
        pattern = r'\\?\$(\w+)'

        def replace_var(match):
            var_name = match.group(1)
            if match.group(0).startswith('\\'):
                return match.group(0)[1:]
            return self.env_vars.get(var_name, '')

        return re.sub(pattern, replace_var, text)

    # Command Functions
    def gset(self, arguments):
        """Set a global environment variable."""
        if len(arguments) != 2:
            print("Usage: gset <key> <value>")
            return
        key, value = arguments
        self.env_vars[key] = value
        print(f"{key} => {value}")

    def gget(self, arguments):
        """Get the value of a global environment variable."""
        if len(arguments) != 1:
            print("Usage: gget <key>")
            return
        key = arguments[0]
        value = self.env_vars.get(key)
        if value is None:
            print(f"{key} is not set.")
        else:
            print(f"{key} => {value}")

    def gsets(self, arguments):
        """Display all global environment variables in a clean format."""
        if not self.env_vars:
            print("No environment variables set.")
            return

        # Dynamically calculate the length of the longest key
        max_key_length = max(len(key) for key in self.env_vars.keys())
        max_val_length = max(len(val) for val in self.env_vars.values())

        first_stat_name = 'Name'
        secondary_stat_name = 'Value'

        if len(first_stat_name) > max_key_length:
            max_key_length = len(first_stat_name)
        if len(secondary_stat_name) > max_val_length:
            max_val_length = len(secondary_stat_name)
        
        # Adjusting the header and separator based on the longest key length
        header = f"{first_stat_name.ljust(max_key_length)}   {secondary_stat_name}"
        separator = f"{'-' * max_key_length}   {'-' * max_val_length}"

        # Prepare the rows with environment variables
        rows = [header, separator]
        for key, value in self.env_vars.items():
            rows.append(f"{key.ljust(max_key_length)}   {value}")

        # Print all rows
        print()
        print("\n".join(rows))
        print()


    def help(self, arguments):
        """Display help for all commands or a specific command."""
        if not arguments:
            # Dynamically set the length for the separator line
            first_stat_name = 'Commands:'
            secondary_stat_name = ''

            # Get the longest command length to format the output
            #max_command_length = max(len(command) for command in self.commands)
            #max_command_length = max(max_command_length, len(first_stat_name))  # Ensure 'cmdname' fits properly

            max_command_length = len(first_stat_name)

            header = f"{first_stat_name.ljust(max_command_length)}   {secondary_stat_name}"
            separator = f"{'=' * max_command_length}   "#{'=' * len(secondary_stat_name)}"
            rows = [header, separator]
            
            # Add all commands and their help text to the rows
            for command, help_message in self.command_help.items():
                rows.append(f"  {command.ljust(max_command_length)}   {help_message}")
            
            # Print all rows as the help content
            print()
            print("\n".join(rows))
        else:
            # Specific command help
            command_name = arguments[0]
            if command_name in self.command_help:
                print(f"{command_name} => {self.command_help[command_name]}")
            else:
                print(f"'{command_name}' is not a recognized command.")
        print()


    def exit(self, arguments):
        """Exit the shell."""
        sys.exit(0)

    def clear(self, arguments):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

# def scanmode_command(arguments, shell_instance):
#     """Activate scan mode."""
#     shell_instance.prompt = "scan> "
# 
# def get_commands():
#     """Return a dictionary of custom commands."""
#     return {
#         "scanmode": {
#             "function": scanmode_command,
#             "help": "Activate scan mode"
#         }
#     }
# 
# def main():
#     """Main entry point for running the shell."""
#     shell_instance = Shell(prompt=">>> ", commands=get_commands())
#     shell_instance.run_shell()
# 
# if __name__ == "__main__":
#     main()
