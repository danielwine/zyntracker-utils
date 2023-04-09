from relive.io.process import get_platform

# [PATHS]
# zss = ., /zynthian/zynthian-my-data/snapshots
# xrns = ., /home/daniel/ideas/

debug_mode = False
autorun_jack = False

platform, _ = get_platform()
isRaspberry = True if platform == 'armv7l' else False
