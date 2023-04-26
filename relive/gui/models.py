
class Status:
    file = ''
    bpm = 120
    bpb = 4
    banks = 0
    patterns = 0
    running_jackd = False
    running_sampler = False

    def __init__(self, file, bpm, banks, patterns,
                 running_jackd, running_sampler) -> None:
        self.file = file
        self.bpm = bpm
        self.banks = banks
        self.patterns = patterns
        self.running_jackd = running_jackd
        self.running_sampler = running_sampler


class Pad:
    pass
