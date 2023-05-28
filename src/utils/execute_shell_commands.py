import subprocess

def execute_shell_commands(commands:str,check:bool = True, quiet:bool=True):
    """
    Executes consecutive shell commands provided as a string.

    Args:
        commands (str): String containing the shell commands separated by semicolons.
        quiet (bool, optional): If True, suppresses the printing of the command output. Defaults to False.

    Returns:
        int: The exit code of the last executed command.
    """
    commands_list = commands.split(';')
    exit_code = 0
    for cmd in commands_list:
        cmd = cmd.strip()
        if quiet:
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            _, _ = process.communicate()
            exit_code = process.returncode
        else:
            exit_code = subprocess.run(cmd, shell=True, check=check).returncode
    return exit_code
