import logging
import time
from json import JSONDecoder
from os.path import dirname, realpath
from relive.shared.tracker import TrackerPattern, TrackerProject
from relive.shared.zss import SnapshotManager
from lib.zynseq import zynseq

basepath = dirname(realpath(__file__))
logger = logging.getLogger(__name__)
ui_scale = 2


class Sequencer(zynseq.zynseq, SnapshotManager):
    def __init__(self):
        super().__init__()
        self.filepath = ""
        self.file = ""

    def initialize(self, path):
        super().initialize(path)
        self.pattern = PatternManager(self.libseq)
        self.get_statistics()

    def import_project(self, file_name, tracker_project):
        self.tracker = tracker_project
        info = self.tracker.info
        self.load('')
        self.libseq.setTempo(int(info['bpm']))
        self.file = file_name

        bank = 1
        self.select_bank(bank)
        self._import_groups(bank)
        self.get_statistics()

    def _expand_pattern(self, phrase):
        line_nr = phrase.line_nr
        if self.libseq.getSteps() < line_nr:
            multiplier = int(line_nr / self.libseq.getSteps())
            self.libseq.setBeatsInPattern(
                self.libseq.getBeatsInPattern() * multiplier)

    def _import_groups(self, bank):
        sequence_nr = 0
        for group_nr, group in enumerate(self.tracker.get_groups()):
            for phrase_nr, phrase in enumerate(group.phrases):
                self.set_sequence_name(
                    bank, sequence_nr, f'{group.name} {phrase_nr}')
                notes = phrase.pattern.get_sequencer_stream()
                pattern_nr = self.libseq.getPattern(bank, sequence_nr, 0, 0)
                self.select_pattern(pattern_nr)
                self._expand_pattern(phrase)
                for step in range(len(notes)):
                    self.libseq.addNote(*notes[step])
                self.libseq.setChannel(bank, sequence_nr, 0, group_nr)
                self.libseq.setGroup(bank, sequence_nr, group_nr)
                sequence_nr += 1

    def get_info_all(self):
        return {
            'sequences': self.get_props_of_sequences(),
            'pattern_info': self.pattern.info(),
            'pattern': self.pattern.get_notes()
        }

    def get_statistics(self):
        ls = self.libseq
        self.bpm = ls.getTempo()
        self.bpb = ls.getBeatsPerBar()
        self.banks = {}
        self.patterns = []
        for bnum in range(1, 255):
            seqs = ls.getSequencesInBank(bnum)
            if seqs:
                self.banks[bnum] = False
                for snum in range(seqs):
                    if not ls.isEmpty(bnum, snum):
                        self.banks[bnum] = True
                        for tnum in range(ls.getTracksInSequence(snum)):
                            self.patterns.append(
                                self.get_pids_in_track(bnum, snum, tnum))

    def get_pids_in_track(self, bnum, snum, tnum):
        ''' iterates over the track and collects pattern indices '''
        location = 0
        patterns = []
        total_patterns = self.libseq.getPatternsInTrack(bnum, snum, tnum)
        while len(patterns) != total_patterns:
            ret = self.libseq.getPattern(bnum, snum, tnum, location)
            if ret != -1:
                patterns.append(ret)
            location += 1
        return patterns

    def get_value(self, expression, default):
        if hasattr(self, expression):
            return getattr(self, expression)
        else:
            return default

    @property
    def pattern_count(self):
        return len([item for sub in self.patterns for item in sub])

    @property
    def statistics(self):
        return {
            'file': None if not self.file else self.file,
            'BPM': self.get_value('bpm', 120.0),
            'BPB': self.get_value('bpb', 4),
            'banks': len(self.get_value('banks', {})),
            'patterns': self.get_value('pattern_count', 0)
        }

    def list_banks(self):
        return self.banks

    @property
    def pattern_info(self):
        return self.pattern.info

    def get_props_of_sequences(self):
        seqs = {}
        if not hasattr(self, 'libseq'):
            return
        for el in range(self.libseq.getSequencesInBank(self.bank)):
            seqs[el] = self.get_props_of_sequence(el)
        return seqs

    def get_props_of_sequence(self, seq_num):
        return {
            'name': self.get_sequence_name(self.bank, seq_num),
            'group': self.libseq.getGroup(self.bank, int(seq_num)),
            'trigger': self.libseq.getTriggerNote(self.bank, seq_num)
        }

    @property
    def sequence_names(self):
        return {key: value['name']
                for key, value in self.get_props_of_sequences().items()}

    def select_pattern(self, pattern):
        return self.pattern.select(pattern)

    def list_patterns(self):
        return self.patterns

    def get_notes_in_pattern(self):
        return self.pattern.notes

    def test_midi(self):
        self.libseq.playNote(62, 110, 0, 200)
        time.sleep(1)
        self.libseq.playNote(74, 110, 0, 200)
        time.sleep(1)

    def load_file(self, path, filename, **args):
        self.file = filename.split(".")[0]
        self.extension = filename.split(".")[1]
        self.filepath = path + "/" + filename
        return self.load_snapshot(self.filepath, **args)

    def save_file(self):
        if not hasattr(self, 'content'):
            self.create_snapshot_from_template(self.file)
        else:
            self.save_snapshot(self.file)

    def start(self):
        pass

    def stop(self):
        self.libseq.setPlayState(0, 0)
        self.libseq.setPlayState(1, 0)


class PatternManager:
    def __init__(self, libseq) -> None:
        super().__init__()
        self.libseq = libseq
        self.id = 0

    def select(self, pattern):
        pattern = int(pattern)
        self.id = pattern
        self.libseq.selectPattern(pattern)

    def import_pattern(self, pattern):
        if not isinstance(pattern, TrackerPattern):
            return False
        stream = pattern.get_sequencer_stream()
        self.notes = stream

    @property
    def info(self):
        ls = self.libseq
        return {
            'steps': ls.getSteps(),
            'beats': ls.getBeatsInPattern(),
            'spb': ls.getStepsPerBeat(),
            'cps': ls.getClocksPerStep(),
            'length': ls. getPatternLength(ls.getPatternIndex()),
            'inprest': ls.getInputRest(),
            'scale': ls.getScale(),
            'tonic': ls.getTonic(),
            'modified': ls.isPatternModified(),
            'refnote': ls.getRefNote(),
            'laststep': ls.getLastStep(),
            'playhead': ls.getPatternPlayhead()
        }

    @property
    def notes(self):
        notes = []
        for step in range(self.libseq.getSteps()):
            isStepEmpty = True
            for note in range(0, 127):
                vel = self.libseq.getNoteVelocity(step, note)
                if vel:
                    notes.append([step, note, vel, self.libseq
                                  .getNoteDuration(step, note)])
                    isStepEmpty = False
            if isStepEmpty:
                notes.append([step])
        return notes

    @notes.setter
    def notes(self, note_list):
        for note in note_list:
            print(note)
            # self.libseq.addNote(note[0], note[1], note[2], note[3])
