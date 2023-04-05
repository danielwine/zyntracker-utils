import __main__

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
