import __main__


class LoggerFactory:
    def __new__(cls, name):
        cls.name = name
        mfile = __main__.__file__.split('/')[-2]
        if mfile == 'cli':
            return cls.getDefaultLogger(cls, name), cls.getName(cls)
        if mfile == 'gui':
            return cls.getKivyLogger(cls), cls.getName(
                cls, default=False)

    def getName(cls, default=True):
        return cls.name.split('.')[-1].capitalize() + ': ' if (
            not default) else ''

    def getKivyLogger(cls):
        from kivy.logger import Logger
        return Logger

    def getDefaultLogger(cls, name):
        import logging
        return logging.getLogger(name)
