import __main__
import logging

ln = ''


class LoggerFactory:
    def __new__(cls, name):
        global ln
        cls.name = name
        mfile = __main__.__file__.split('/')[-2]
        if mfile == 'cli':
            ln = cls.getName(cls)
            return cls.getDefaultLogger(cls, name)
        if mfile == 'gui':
            ln = cls.getName(cls, default=False)
            return cls.getKivyLogger(cls)

    def getName(cls, default=True):
        return cls.name.split('.')[-1].capitalize() + ': ' if (
            not default) else ''

    def getKivyLogger(cls):
        from kivy.logger import Logger
        return Logger

    def getDefaultLogger(cls, name):
        import logging
        return logging.getLogger(name)


def format(message):
    if ln != '' and message.startswith('  '):
        message = message[2:]
    return f'{ln}{message}'


# class CursesLogger:
#     def register_screen(self, screen):
#         self.screen = screen

#     def info(self, message):
#         self.screen.addstr(1,0, message)


try:
    unicode
    _unicode = True
except NameError:
    _unicode = False


class CursesHandler(logging.Handler):
    def __init__(self, screen):
        logging.Handler.__init__(self)
        self.screen = screen

    def emit(self, record):
        try:
            msg = self.format(record)
            screen = self.screen
            fs = "\n%s"
            if not _unicode:  # if no unicode support...
                screen.addstr(fs % msg)
                screen.refresh()
            else:
                try:
                    if (isinstance(msg, unicode)):
                        ufs = u'\n%s'
                        try:
                            screen.addstr(ufs % msg)
                            screen.refresh()
                        except UnicodeEncodeError:
                            screen.addstr((ufs % msg).encode(code))
                            screen.refresh()
                    else:
                        screen.addstr(fs % msg)
                        screen.refresh()
                except UnicodeError:
                    screen.addstr(fs % msg.encode("UTF-8"))
                    screen.refresh()
            if 'active_line' in screen:
                screen.active_line += 1
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
