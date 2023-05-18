from os.path import dirname, abspath

# General settings

debug_mode = False
autorun_jack = False

# Sequencer (importer) settings

create_backup = True
auto_bank = 10
trigger_channel = 15
trigger_start_note = 24

# Paths

PATH_BASE = dirname(abspath(__file__))
PATH_DATA = '/'.join(PATH_BASE.split('/')[:-1]) + '/data'
PATH_ZSS = PATH_DATA + '/zss'
PATH_XRNS = '/home/daniel/xrns/zynedit'
PATH_PROJECTS = PATH_DATA + '/projects'

PATH_ZSS_REMOTE = '/zynthian/zynthian-my-data/snapshots/'
PATH_SAMPLES = '/zynthian/zynthian-data/soundfonts/'
PATH_SAMPLES_MY = '/zynthian/zynthian-my-data/soundfonts/'

SFTP_HOST = "zynthian.local"
SFTP_USER = "root"
SFTP_PASSWORD = "raspberry"
SFTP_DEFAULT_SNAPSHOT = '001'
