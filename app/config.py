from os.path import dirname, abspath

debug_mode = False
autorun_jack = False

PATH_BASE = dirname(abspath(__file__))
PATH_DATA = '/'.join(PATH_BASE.split('/')[:-1]) + '/data'
PATH_ZSS = PATH_DATA + '/zss'
PATH_XRNS = '/home/daniel/xrns/zynedit'
PATH_PROJECTS = PATH_DATA + '/projects'

PATH_SAMPLES = '/zynthian/zynthian-data/soundfonts/'
PATH_SAMPLES_MY = '/zynthian/zynthian-my-data/soundfonts/'
