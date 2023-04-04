import logging
from sys import stdout
from os.path import isfile, join
from os import listdir, getcwd
from .commands import pcmds, lcmds
from .errors import InvalidArgumentType, MissingArgument
from relive.audio.service import AudioManager

logging.basicConfig(stream=stdout, level=logging.INFO,
                    format='%(message)s')
logger = logging.getLogger()


class CLI:
    file = ''

    def __init__(self) -> None:
        print('Interactive shell for zynseq by danielwine.')
        print('h: help, x: exit, enter: previous cmd')
        print('  usage <cmd> [options]')
        print('   e.g.: pn 62 110 0 200')

    def start(self):
        self.audio = AudioManager(init_delay=0.2, verbose=True)
        self.audio.start()
        self.print_statistics()
        self.console_loop()

    def pprint(self, data):
        if type(data) == dict:
            for key, value in data.items():
                key = f'{key}'
                value = 'empty' if value == False else value
                print(f"  {key:<5s} : {value}")
        if type(data) == list:
            for el in data:
                print(f"  {el}")

    def show_help(self):
        cmds = {}
        for method in CLI.__dict__.items():
            if method[0].startswith('cmd_'):
                cmds[method[0][4:]] = method[1].__doc__
        self.pprint(cmds)
        self.pprint(pcmds)
        print()
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
            print('Please specify file name.')
            return
        files = [el for el in self.zss() if el.startswith(par[0])]
        self.file = files[0] if files else ''
        if self.file:
            success = self.audio.seq.load_file(
                getcwd() + '/data/zss', self.file)
            if success:
                self.audio.seq.get_info()
                self.print_statistics()
        # self.info(4)

    def print_statistics(self):
        print('FILE loaded: ', 'none' if not self.file else self.file)
        print(f'  {"BPM:":9s}', self.audio.seq.bpm)
        print(f'  {"BPB:":9s}', self.audio.seq.bpb)
        print(f'  {"banks:":9s}', len(self.audio.seq.banks))
        print(f'  {"patterns:":9s}', self.audio.seq.get_pattern_count())

    def zss(self):
        zss = self.get_files('./data/zss')
        zss.sort()
        return zss

    def parse_libcmds(self, cmd, par):
        fnsplit = lcmds[cmd].split()
        fname = fnsplit[0]
        try:
            func = getattr(self.audio.seq.libseq, fname)
            ret = self.invoke_lib_function(func, fnsplit[1:], par)
            print(ret)
        except InvalidArgumentType as e:
            print('Invalid argument.', e)
        except MissingArgument as e:
            print('Missing argument:', e)
        except AttributeError as e:
            print(e)

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
                print(ret)

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
        ports = self.audio.client.get_ports()
        for port in ports:
            cons = self.audio.client.get_all_connections(port)
            if cons:
                print(port)
                self.pprint(cons)

    def cmd_proc(self, par):
        """list running engines"""
        self.audio.check_services()

    def cmd_info(self, par):
        """print statistics"""
        self.print_statistics()

    def console_loop(self):
        quit = False
        prev_res = ''
        while not quit:
            res = input(
                f'b{self.audio.seq.bank:02d}p{self.audio.seq.pattern:02d}> ')
            res = res.strip()
            if res == '':
                res = prev_res
            else:
                prev_res = res
            rsplit = res.split(' ')
            cmd = rsplit[0]
            par = rsplit[1:] if len(rsplit) > 1 else ''
            if cmd in ['x', 'exit', 'quit']:
                quit = True
            if cmd in ['h', 'help']:
                self.show_help()
            if hasattr(self, 'cmd_' + cmd):
                getattr(self, 'cmd_' + cmd)(par)
            if cmd in lcmds:
                self.parse_libcmds(cmd, par)
            if cmd in pcmds:
                self.parse_pycmds(cmd, par)

    def stop(self):
        self.audio.stop()
