
class Note:
    NOTES = ["C", "C#", "D", "D#", "E",
             "F", "F#", "G", "G#", "A", "A#", "B"]
    OFFNOTE = 'OFF'
    EMPTY = '---'

    def __init__(self, midi_note=0, velocity=0, duration=0) -> None:
        self.midi = midi_note
        self.velocity = velocity
        self.duration = duration

    def __repr__(self) -> str:
        return f'{Note.get_string(self.midi)}, ' \
           f'{self.velocity}, {self.duration}'

    @property
    def values(self):
        return [self.midi, self.velocity, self.duration]

    @classmethod
    def get_string(cls, code):
        code = int(code)
        if code < 23:
            return cls.EMPTY
        if code == -1:
            return cls.OFFNOTE
        code = code - 24
        octave = int(code / 12)
        note = Note.NOTES[code % 12]
        sep = '-' if not note.endswith('#') else ''
        return f'{note}{sep}{octave}'

    @classmethod
    def get_midi(cls, note):
        if note == cls.OFFNOTE:
            return -1
        octave = note[-1]
        note = note[:-1].strip('-')
        code = 24 + int(octave) * 12 + Note.NOTES.index(note)
        return code


class TrackerPattern:
    def __init__(self, line_number=0, notes=[]) -> None:
        self._notes = {}
        self.line_number = line_number
        self.duration_measure = 4
        if line_number > 0 and notes:
            self.add_notes(notes)
            self.get_all_note_durations()

    def __repr__(self) -> str:
        return []

    def add_notes(self, notes):
        for step, cnotes in notes.items():
            cnotes_target = []
            for note in cnotes:
                cnotes_target.append(note)
            self._notes[step] = cnotes_target

    @property
    def notes(self):
        return self._notes

    @property
    def polyphony_level(self):
        return max([len(notes) for step, notes in self._notes.items()])

    def get_note_at(self, note_line, note_col):
        if note_line not in self._notes:
            return False
        line = self._notes[note_line]
        if len(line) < note_col + 1:
            return False
        if line[note_col] == None:
            return False
        else:
            return line[note_col]

    def get_all_note_durations(self):
        for column in range(self.polyphony_level):
            last_step = 0
            last_note = Note()
            items = self._notes.items()
            for step, notes in items:
                if step >= self.line_number:
                    # don't calculate durations for invisible notes
                    last_note.duration = self.line_number - last_step
                    break
                if len(notes) < column + 1:
                    continue
                if notes[column] is not None:
                    last_note.duration = step - last_step
                    last_note = notes[column]
                    last_step = step
            last_note.duration = self.line_number - last_step

    def _get_note_duration_for(self, note_line, note_col):
        if not self.get_note_at(note_line, note_col):
            return
        steps = list(self._notes.keys())
        sidx = steps.index(note_line)
        for line_nr in steps[sidx+1:]:
            ln = self._notes[line_nr]
            if len(ln) < note_col + 1:
                continue
            cn = self._notes[line_nr][note_col]
            if cn is not None:
                # print('INTERRUPT! ', line_nr, note_col)
                return line_nr - note_line

    def get_sequencer_stream(self):
        lines = []
        for step in range(self.line_number):
            if step in self._notes:
                for note in self._notes[step]:
                    if note is not None and note.midi != -1:
                        l = [step, note.midi,
                             note.velocity,
                             note.duration / self.duration_measure]
                        lines.append(l)
        return lines

    def get_tracker_stream(self):
        pass


class TrackerPhrase:
    def __init__(self, **kwargs) -> None:
        self.name = kwargs['name']
        self.preset = kwargs['preset']
        self.lpb = kwargs['lpb']
        self.line_nr = int(kwargs['#lines'])
        self._notes = []
        self.add_notes(kwargs['notes'])

    def add_notes(self, notes):
        self._notes = TrackerPattern(self.line_nr, notes)

    @property
    def pattern(self):
        return self._notes

    @property
    def notes(self):
        return self._notes.notes


class TrackerGroup:
    def __init__(self, name, phrases) -> None:
        self.name = name
        self.phrases = []
        self.add_phrases(phrases)

    def add_phrases(self, phrases):
        for phrase in phrases:
            self.phrases.append(TrackerPhrase(**phrase))


class TrackerProject:
    def __init__(self, info={}, groups=[]) -> None:
        self.info = info
        if type(groups) is not list:
            raise TypeError
        self._groups = []
        self.add_info(info)
        self.add_groups(groups)

    def add_info(self, info):
        self.info = info

    def add_groups(self, groups):
        for group in groups:
            self._groups.append(TrackerGroup(**group))

    def get_group(self, number):
        return self._groups[number]
