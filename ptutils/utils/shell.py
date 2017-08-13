"""
Utilities for running shell scripts and interacting with the terminal
"""
import sys
import subprocess as sp


def run_shell_command(cmd):
    """
    Runs cmd as a shell command. Waits for it to finish executing,
    then returns all output printed to standard error and standard out,
    and the return code.
    Parameters
    ----------
    cmd : str
        The shell command to run
    Returns
    -------
    output : str
        The string output of the process
    rc : WRITEME
        The numeric return code of the process
    """
    child = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.STDOUT)
    output = child.communicate()[0]
    rc = child.returncode
    return output, rc


def execute_process(command_shell):
    stdout = sp.check_output(command_shell, shell=True).strip()
    if not isinstance(stdout, (str)):
        stdout = stdout.decode()
    return stdout
