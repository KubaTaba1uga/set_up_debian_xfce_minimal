from time import sleep

from src.process import Process


def test_is_alive(popen_process):
    assert Process.is_alive(popen_process.pid) is True
    popen_process.terminate()


def test_is_sleeping(popen_process):
    sleep(0.1)
    assert Process.is_sleeping(popen_process.pid) is True
    popen_process.terminate()


def test_kill(popen_process):
    Process.kill(popen_process.pid)
    sleep(0.3)
    popen_process.poll()
    assert Process.is_alive(popen_process.pid) is False
