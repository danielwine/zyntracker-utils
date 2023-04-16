
from os.path import isfile, join
from os import listdir, getcwd
from .commands import pcmds, lcmds
from .errors import InvalidArgumentType, MissingArgument
from relive.audio.utils import is_port, format_port


class REPL:
    MSG_HEADER = 'zyntracker / zynseq interactive shell by danielwine.'
    MSG_USAGE = 'h: help, x: exit, enter: previous cmd' \
        '\n  usage <cmd> [options]' \
        '\n   e.g.: pn 62 110 0 200'

    def __init__(self):
        self.print = print
        self.events = {}

    def set_dir(self, snapshot_path):
        self.snapshot_path = snapshot_path

    def set_print_callback(self, cb):
        self.print = cb

    def register_event(self, event, cb):
        self.events[event] = cb

    def call_event_callback(self, event):
        if event in self.events:
            self.events[event]()

    def pprint(self, data):
        if type(data) == dict:
            for key, value in data.items():
                key = f'{key}'
                value = 'empty' if value == False else value
                self.print(f"  {key:<5s} : {value}")
        if type(data) == list:
            for el in data:
                if type(el) == tuple:
                    if is_port(el[0]):
                        self.print(format_port(el[0]))
                        for port in el[1]:
                            self.print('  ' + format_port(port))
                    else:
                        self.print(f"  {el[0]}: {el[1]}")
                else:
                    if is_port(el):
                        self.print('  ' + format_port(el))
                    else:
                        self.print(f"  {el}")

    def mprint(self, data):
        self.print('  ' + ' '.join([key for key in data.keys()]))

    def show_help(self, basic=False):
        cmds = {}
        for method in REPL.__dict__.items():
            if method[0].startswith('cmd_'):
                cmds[method[0][4:]] = method[1].__doc__
        if basic:
            self.mprint(cmds)
            self.mprint(pcmds)
            return
        self.pprint(cmds)
        self.pprint(pcmds)
        self.print('')
        self.pprint(lcmds)

    def convert_params(self, par, specs):
        ret = []
        for num, typ in enumerate(specs):
            if typ == 'i':
                if par[num].isnumeric():
                    ret.append(int(par[num]))
                else:
                    raise InvalidArgumentType('numeric value')
            if typ == 'b':
                nm = int(par[num])
                if nm >= 0 and nm < 2:
                    ret.append(False if nm == 0 else True)
                else:
                    raise InvalidArgumentType('boolean')
        return ret

    def invoke_lib_function(self, fn, specs, p):
        if len(p) < len(specs):
            arg = specs[len(p)]
            raise MissingArgument(arg)
        p = self.convert_params(p, specs)
        lp = len(p)
        if lp == 0:
            r = fn()
        if lp == 1:
            r = fn(p[0])
        elif lp == 2:
            r = fn(p[0], p[1])
        elif lp == 3:
            r = fn(p[0], p[1], p[2])
        elif lp == 4:
            r = fn(p[0], p[1], p[2], p[3])
        elif lp == 5:
            r = fn(p[0], p[1], p[2], p[3], p[4])
        return r

    def get_files(self, path):
        return [f for f in listdir(path) if isfile(join(path, f))]

    def load(self, par):
        if not par:
            self.print('Please specify file name.')
            return
        files = [el for el in self.zss() if el.startswith(par[0])]
        self.file = files[0] if files else ''
        if self.file:
            success = self.audio.seq.load_file(
                getcwd() + '/data/zss', self.file)
            if success:
                self.audio.seq.get_statistics()
                event = 'file_loaded'
                if event in self.events:
                    self.call_event_callback('file_loaded')
                else:
                    self.pprint(self.audio.seq.statistics)

    def zss(self):
        if not self.snapshot_path:
            return []
        zss = self.get_files(self.snapshot_path)
        zss.sort()
        return zss

    def parse_libcmds(self, cmd, par):
        fnsplit = lcmds[cmd].split()
        fname = fnsplit[0]
        try:
            func = getattr(self.audio.seq.libseq, fname)
            ret = self.invoke_lib_function(func, fnsplit[1:], par)
            self.print(ret)
        except InvalidArgumentType as e:
            self.print('Invalid argument.', e)
        except MissingArgument as e:
            self.print('Missing argument:', e)
        except AttributeError as e:
            self.print(e)

    def parse_pycmds(self, cmd, par):
        fnsplit = pcmds[cmd].split()
        fname = fnsplit[0]
        func = getattr(self.audio.seq, fname)
        par = self.convert_params(par, fnsplit)
        if len(fnsplit) == 1:
            ret = func()
        if len(fnsplit) > 1:
            ret = func(*par)
        if ret:
            if type(ret) is list or type(ret) is dict:
                self.pprint(ret)
            else:
                self.print(ret)

    def cmd_dir(self, par):
        """list ZSS files"""
        self.pprint(self.zss())

    def cmd_load(self, par):
        """load ZSS file"""
        self.load(par)

    def cmd_ports(self, par):
        """list available jack ports"""
        self.pprint(self.audio.client.get_ports())

    def cmd_cons(self, par):
        """list jack connections"""
        self.pprint(self.audio.get_all_connections())

    def cmd_proc(self, par):
        """list running engines"""
        self.audio.check_services()

    def cmd_info(self, par):
        """print statistics"""
        self.pprint(self.audio.seq.statistics)

    def evaluate(self, res):
        rsplit = res.split(' ')
        cmd = rsplit[0]
        par = rsplit[1:] if len(rsplit) > 1 else ''
        if cmd in ['x', 'exit', 'quit']:
            return False
        if cmd in ['h', 'help']:
            self.show_help()
        if hasattr(self, 'cmd_' + cmd):
            getattr(self, 'cmd_' + cmd)(par)
        if cmd in lcmds:
            self.parse_libcmds(cmd, par)
        if cmd in pcmds:
            self.parse_pycmds(cmd, par)
        return True
