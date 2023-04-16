import os
from os.path import dirname, realpath, exists
from subprocess import Popen, PIPE


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


def launch_plugin(url, debug):
    if not debug: stdout.mute()
    proc = Popen(['jalv', url], stdin=PIPE, stdout=PIPE)
    if not debug: stdout.unmute()
    return proc


def _popen_pipe(app, param=''):
    proc = Popen([app, param], stdout=PIPE)
    ret, err = proc.communicate()
    return ret.decode('utf-8').strip(), err


def kill(pid):
    if type(pid) == 'string':
        return _popen_pipe('kill', pid)
    elif type(pid) is list:
        for item in pid:
            if item:
                _popen_pipe('kill', item)


def get_process_id(name):
    return _popen_pipe('pgrep', name)


def get_platform():
    return _popen_pipe('uname', '-m')


def guess_engine():
    ret, err = get_process_id('renoise')
    return 'renoise' if ret else 'zynaddsubfx'


def get_context():
    zynthian_root = os.environ.get('ZYNTHIAN_DIR') or ''
    zynthian_path = zynthian_root + '/zynthian-ui/zynlibs/zynseq'
    build_path = '/build/libzynseq.so'
    local_path = dirname(realpath(__name__))
    zynthian_full_path = zynthian_path + build_path
    local_full_path = local_path + '/lib/zynseq' + build_path
    if exists(zynthian_full_path):
        return {
            'zynthian': True,
            'path_lib': zynthian_full_path,
            'path_snapshot': zynthian_root
            + '/zynthian-my-data/snapshots/000',
            'audio': 'zynmidirouter'
        }
    if exists(local_full_path):
        return {
            'zynthian': False,
            'path_lib': local_full_path,
            'path_snapshot': local_path + '/data/zss',
            'audio': guess_engine()
        }


stdout = StdOut()
