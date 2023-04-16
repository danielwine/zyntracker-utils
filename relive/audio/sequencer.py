import base64
import time
import logging
from json import JSONDecoder
from os.path import dirname, realpath
from relive.shared.tracker import TrackerPattern
from lib.zynseq import zynseq

basepath = dirname(realpath(__file__))
logger = logging.getLogger(__name__)
ui_scale = 2

class SnapshotManager:
    def __init__(self):
        self.content = {}

    def load_snapshot(self, fpath, load_sequence=True):
        if load_sequence: logger.debug('Loading ' + fpath)
        try:
            with open(fpath, "r") as fh:
                json = fh.read()
                logger.debug(f"Loading snapshot {fpath}")
                logger.debug(f"=> {json}")

        except Exception as e:
            logger.error("Can't load snapshot '%s': %s" % (fpath, e))
            return False

        try:
            snapshot = JSONDecoder().decode(json)
            self.content = snapshot
            if "zynseq_riff_b64" in snapshot:
                b64_bytes = snapshot["zynseq_riff_b64"].encode("utf-8")
                binary_riff_data = base64.decodebytes(b64_bytes)
                if not load_sequence:
                    return True
            else:
                return False
            self.restore_riff_data(binary_riff_data)
            return True

        except Exception as e:
            logger.exception("Invalid snapshot: %s" % e)
            return False


class Sequencer(zynseq.zynseq, SnapshotManager):
    def __init__(self):
        super().__init__()
        self.filepath = ""
        self.file = ""

    def initialize(self, path):
        super().initialize(path)
        self.pattern = PatternManager(self.libseq)
        self.get_statistics()

    def get_info_all(self):
        return {
            'sequences': self.list_sequences_in_bank(),
            'pattern_info': self.pattern.get_info(),
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
        location = 0
        patterns = []
        total_patterns = self.libseq.getPatternsInTrack(bnum, snum, tnum)
        while len(patterns) != total_patterns:
            ret = self.libseq.getPattern(bnum, snum, tnum, location)
            if ret != -1: patterns.append(ret)
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
            'file': "none" if not self.file else self.file,
            'BPM': self.get_value('bpm', 120.0),
            'BPB': self.get_value('bpb', 4),
            'banks': len(self.get_value('banks', {})),
            'patterns': self.get_value('pattern_count', 0)
        }

    def list_banks(self):
        return self.banks

    @property
    def sequences_in_bank(self):
        seqs = {}
        for el in range(self.libseq.getSequencesInBank(self.bank)):
            seqs[el] = self.get_sequence_name(self.bank, el)
        return seqs

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

    # def save(self):
    #     self.libseq.save(bytes(self.filepath, "utf-8"))

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

    @property
    def info(self):
        ls = self.libseq
        return {
            'steps': ls.getSteps(),
            'beats': ls.getBeatsInPattern(),
            'length': ls. getPatternLength(ls.getPatternIndex()),
            'cps': ls.getClocksPerStep(),
            'spb': ls.getStepsPerBeat(),
            'inpch': ls.getInputChannel(),
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
            for note in range(0,127):
                vel = self.libseq.getNoteVelocity(step,note)
                if vel: 
                    notes.append([step, note, vel, self.libseq
                        .getNoteDuration(step, note)])
                    isStepEmpty = False
            if isStepEmpty: notes.append([step])
        return notes
