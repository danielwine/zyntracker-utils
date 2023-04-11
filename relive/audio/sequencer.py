import base64
import time
import logging
from json import JSONDecoder
from os.path import dirname, realpath
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
        self.pattern = 0

    def initialize(self, path):
        super().initialize(path)
        self.get_info()

    def get_info(self):
        self.bpm = self.libseq.getTempo()
        self.bpb = self.libseq.getBeatsPerBar()
        self.get_statistics()

    def get_statistics(self):
        ls = self.libseq
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

    @property
    def pattern_count(self):
        return len([item for sub in self.patterns for item in sub])

    def list_banks(self):
        return self.banks

    def list_sequences_in_bank(self):
        seqs = {}
        for el in range(self.libseq.getSequencesInBank(self.bank)):
            seqs[el] = self.get_sequence_name(self.bank, el)
        return seqs

    def list_patterns(self):
        return self.patterns

    def select_pattern(self, pattern):
        pattern = int(pattern)
        self.pattern = pattern
        self.libseq.selectPattern(pattern)

    def get_notes_track(self):
        for track in range(self.tracks):
            sequence_id = self.libseq.getSequence(self.song, track)
            first_pattern = self.libseq.getPattern(sequence_id, 0)
            self.libseq.selectPattern(first_pattern)
            self.notes_track[track] = self.scan_notes()

    def get_pattern_info(self):
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

    def get_notes_in_pattern(self):
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

    def get_steps(self, track):
        # libseq.selectPattern(self.pattern_ids[track])
        # return libseq.getSteps()
        return 32

    def get_channel(self, track):
        # sequence_id = libseq.getSequence(self.song, track)
        # return sequence_id, libseq.getChannel(sequence_id)
        pass

    def get_pattern_ids(self):
        for pad in range(self.tracks):
            sequence = self.libseq.getSequence(self.song, pad)
            self.pattern_ids.append(self.libseq.getPattern(sequence, 0))

    def test_midi(self):
        self.libseq.playNote(62, 110, 0, 200)
        time.sleep(1)
        self.libseq.playNote(74, 110, 0, 200)
        time.sleep(1)

    def load_file(self, path, filename, **args):
        self.filename = filename.split(".")[0]
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
