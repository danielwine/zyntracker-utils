
pcmds = {
    'test': 'test_midi',
    'lb': 'list_banks',
    'ls': 'sequences_in_bank',
    'lp': 'list_patterns',
    'sb': 'select_bank i',
    'sp': 'select_pattern i',
    'pi': 'pattern_info',
    'pp': 'get_notes_in_pattern',
    'start': 'transport_start',
    'stop': 'transport_stop',
    'toggle': 'transport_toggle'
}

lcmds = {
    'im': 'isModified',
    'ed': 'enableDebug b',
    # Direct MIDI interface
    'pn': 'playNote i i i i',
    # Pattern management
    'cp': 'createPattern',
    'gpt': 'getPatternsInTrack i i i',
    'gs': 'getSteps',
    # Sequence management
    'gsn': 'getSequenceName i i',
    'gts': 'getTracksInSequence i i',
    'tps': 'togglePlayState i i',
    # Bank management
    'gsb': 'getSequencesInBank i',
    't': 'getTempo',
    'tgps': 'transportGetPlayStatus',
}

menu = {
    'F1': 'Window',
    'F9': 'Commands',
    'F10': 'Exit'
}
