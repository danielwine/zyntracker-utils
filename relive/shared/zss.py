import base64
from json import JSONDecoder
import logging

logger = logging.getLogger(__name__)


class SnapshotManager:
    def __init__(self):
        self.content = {}

    def load_snapshot(self, fpath, load_sequence=True):
        if load_sequence:
            logger.debug('Loading ' + fpath)
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
