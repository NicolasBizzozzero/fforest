import subprocess
import sys


def eprint(*args, **kwargs):
    """ Print wrapper for `stderr`. """
    print(*args, file=sys.stderr, **kwargs)


def execute(command: str, *parameters: str, stdin=None, stdout=None, stderr=None) -> int:
    """ Execute `command` in a subprocess and return the result code of the command. """
    result = subprocess.run([command, *parameters], stdin=stdin, input=None, stdout=stdout, stderr=stderr, shell=False,
                            timeout=None, check=False)
    return_code = result.returncode
    return return_code


def execute_and_get_stdout(command: str, *parameters: str, stdin=None, stderr=None, encoding: str = "utf8") -> str:
    """ Execute `command` in a subprocess and return all the output from stdout of the command.

        Example:
            >>> execute_and_get_stdout("printf", "Hello World !")
            'Hello World !'
    """
    try:
        return subprocess.check_output([command, *parameters], stdin=stdin, stderr=stderr, shell=False,
                                       timeout=None).decode(encoding)
    except subprocess.CalledProcessError as error:
        print(error.output)
