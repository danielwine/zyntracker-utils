from os.path import dirname, abspath

# General settings

debug_mode = False
autorun_jack = False

# Sequencer (bridge) settings

create_backup = True       # whether to make a local backup of a zss

vertical_zoom  = 16        # default vertical zoom for saving snapshots
minimum_rows = 5           # minimum number of rows / columns per bank
maximum_rows = 5           # maximum number of rows / columns per bank
auto_bank = 10             # destination bank of auto transposed phrases
trigger_channel = 15       # global trigger channel for sequences
trigger_start_note = 24    # start note for auto transposed sequences

# Paths

PATH_BASE = dirname(abspath(__file__))
PATH_DATA = '/'.join(PATH_BASE.split('/')[:-1]) + '/data'
PATH_ZSS = PATH_DATA + '/zss'
PATH_XRNS = '/home/daniel/xrns/zynedit'
PATH_PROJECTS = PATH_DATA + '/projects'

PATH_ZSS_REMOTE = '/zynthian/zynthian-my-data/snapshots/'
PATH_SAMPLES = '/zynthian/zynthian-data/soundfonts/'
PATH_SAMPLES_MY = '/zynthian/zynthian-my-data/soundfonts/'

# Zynthian configuration

SFTP_HOST = "zynthian.local"
SFTP_USER = "root"
SFTP_PASSWORD = "raspberry"
SFTP_DEFAULT_SNAPSHOT = '003'
