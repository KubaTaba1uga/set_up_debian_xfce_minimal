from time import sleep


def test_delete(temp_err_buffer, bash_shell):
    with bash_shell as shell:
        shell.send_command(f"cat nothing 2> {temp_err_buffer.path}")
        sleep(0.1)
        temp_err_buffer.delete()
        assert temp_err_buffer.path.exists() is False


def test_ctx_manager(temp_err_buffer, bash_shell):
    with bash_shell as shell:
        shell.send_command(f"cat nothing 2> {temp_err_buffer.path}")
        with temp_err_buffer:
            sleep(0.1)
            assert temp_err_buffer.path.exists() is True
        sleep(0.1)
        assert temp_err_buffer.path.exists() is False


def test_read(temp_err_buffer, bash_shell):
    with bash_shell as shell:
        shell.send_command(f"cat nothing 2> {temp_err_buffer.path}")
        with temp_err_buffer:
            sleep(0.1)
            output = temp_err_buffer.read()
    assert "No such file or directory" in output


def test_exist(temp_err_buffer, bash_shell):
    with bash_shell as shell:
        shell.send_command(f"cat nothing 2> {temp_err_buffer.path}")
        with temp_err_buffer:
            sleep(0.1)
            assert temp_err_buffer.exist() is True


def test_create_error_redirection(temp_err_buffer, bash_shell):
    error_redir = temp_err_buffer.create_error_redirection()
    with bash_shell as shell:
        shell.send_command(f"cat nothing {error_redir}")
        with temp_err_buffer:
            sleep(0.1)
            assert temp_err_buffer.path.exists() is True
