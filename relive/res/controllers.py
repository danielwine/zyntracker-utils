
class KeyboardInput:
    def __init__(self, target, layout_even=False):
        self.startnote_a = 48
        self.startnote_b = 60
        self.octave = 3
        self.OCTAVE_INC = ord('*')
        self.OCTAVE_DEC = ord('/')
        self.BPM_INC = 43
        self.BPM_DEC = 45
        self.START_STOP = ord(' ')
        self.DOWN = 258
        self.UP = 259
        self.LEFT = 260
        self.RIGHT = 261
        self.ENTER = 10
        self.HOME = 262
        self.PGDOWN = 338
        self.PGUP = 339
        self.CTRL_HOME = 535
        self.CTRL_END = 530
        self.TAB = b'^I'
        self.SHIFT_TAB = b'KEY_BTAB'
        self.F1 = 265
        self.F2 = 266
        self.END = 360
        self.CTRL_A = b'^A'
        self.ALT_T = b'^['
        self.layout_even = layout_even
        # hu-characters: 'ysxdcvgbhnjm,l.é-', 'q2w3er5t6z7ui9oöpőóú' -=e
        if not layout_even and target == 'GUI':
            self.row_a = [24,11,25,12,26,27,14,28,15,29,16,30,31,
                          18,32,19,33,34,21,35,64]
            self.row_b = [52,39,53,40,54,55,42,56,43,57,44,58,59,46,60,47,61,64]
        if not layout_even and target == 'CLI':
            self.row_a = [121,115,120,100,99,118,103,98,104,110,106,
                          109,44,108,46,169,45]
            self.row_b = [113,50,119,51,101,114,53,116,54,122,55,117,105,57,
                          111,182,112,145,179,186]
        if layout_even and target == 'CLI':
            self.keys = [121,120,99,118,98,110,109,44,46,45,
                         97,115,100,102,103,104,106,107,108,169,161,
                         113,119,101,114,116,122,117,105,111,112,145,186,177]

    def get_midi_note(self, key):
        # print(key)
        if self.layout_even:
            if key in self.keys:
                return self.keys.index(key)
            else: return False
        else:
            if key in self.row_a:
                pos = self.row_a.index(key)
                return self.startnote_a + pos
            if key in self.row_b:
                pos = self.row_b.index(key)
                return self.startnote_b + pos
            else: return False
