import os
from subprocess import Popen, PIPE

# sys.stdout = io.StringIO()
# sys.stderr = io.StringIO()


class StdOut:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(StdOut, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.muted = False

    def mute(self):
        if self.muted:
            return
        self.null_fds = [
            os.open(os.devnull, os.O_RDWR) for x in range(2)]
        self.save_fds = [os.dup(1), os.dup(2)]

        os.dup2(self.null_fds[0], 1)
        os.dup2(self.null_fds[1], 2)
        self.muted = True

    def unmute(self):
        if not self.muted:
            return
        os.dup2(self.save_fds[0], 1)
        os.dup2(self.save_fds[1], 2)
        for fd in self.null_fds + self.save_fds:
            os.close(fd)
        self.muted = False


def launch_plugin(uri, debug=False):
    if not debug:
        stdout.mute()
    ret = Popen(['jalv', '-i', uri])
    if not debug:
        stdout.unmute()
    return ret


def _popen_pipe(app, param=''):
    proc = Popen([app, param], stdout=PIPE)
    ret, err = proc.communicate()
    return ret.decode('utf-8').strip(), err

def launch_and_get_code(name):
    return _popen_pipe('pgrep', name)

def kill(pid):
    return _popen_pipe('kill', pid)

def get_platform():
    return _popen_pipe('uname', '-m')


stdout = StdOut()
