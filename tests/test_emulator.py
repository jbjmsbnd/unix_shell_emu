from src.emulator import execute_command


def test_ls():
    assert execute_command("ls") == "ls"


def test_ls_with_argument():
    result = execute_command("ls /home")
    assert result == "ls /home"


def test_cd():
    assert execute_command("cd") == "cd"


def test_cd_with_argument():
    result = execute_command("cd /home")
    assert result == "cd /home"


def test_unknown_command():
    result = execute_command("hello")
    assert result == "Error: unknown command: hello"


def test_invalid_ls_arguments():
    result = execute_command("ls one two")
    assert result == "Error: ls: invalid number of arguments"


def test_invalid_cd_arguments():
    result = execute_command("cd one two")
    assert result == "Error: cd: invalid number of arguments"


def test_exit():
    assert execute_command("exit") == "EXIT"
