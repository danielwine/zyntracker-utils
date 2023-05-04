
lv2_engines_available = {
    'zynaddsubfx': {
        'name': 'ZynAddSubFX',
        'uri': 'http://zynaddsubfx.sourceforge.net'
    },
    'helm': {
        'name': 'Helm',
        'uri': 'http://tytel.org/helm'
    }
}

engines = {k: v for k, v in lv2_engines_available.items() if k == 'zynaddsubfx'}

use_linuxsampler = True
