import psutil


class Process(psutil.Process):
    @classmethod
    def is_alive(cls, pid: int) -> bool:
        return psutil.pid_exists(pid)

    @classmethod
    def is_sleeping(cls, pid: int) -> bool:
        if pid == -1:
            # For testing purposes
            return True
        if cls.is_alive(pid):
            return cls(pid).status() == "sleeping"
        return False

    @classmethod
    def kill(cls, pid: int):
        if cls.is_alive(pid):
            cls(pid).terminate()
