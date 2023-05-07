from os.path import dirname, abspath
from app.io.process import get_platform

debug_mode = False
autorun_jack = False

platform, _ = get_platform()
isRaspberry = True if platform == 'armv7l' else False

PATH_BASE = dirname(abspath(__file__))
PATH_DATA = '/'.join(PATH_BASE.split('/')[:-1]) + '/data'
PATH_XRNS = PATH_DATA + '/xrns'
PATH_PROJECTS = PATH_DATA + '/projects'

PATH_SAMPLES = '/zynthian/zynthian-data/soundfonts/'
PATH_SAMPLES_MY = '/zynthian/zynthian-my-data/soundfonts/'