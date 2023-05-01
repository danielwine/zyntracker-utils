import base64
from os.path import splitext, exists
from json import JSONDecoder, JSONEncoder
from relive.config import PATH_BASE, PATH_DATA
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

    def create_snapshot_from_template(self, file_name):
        self.load_snapshot(PATH_BASE + '/shared/base.zss', load_sequence=False)
        self.save_snapshot(splitext(file_name)[0])

    def save_snapshot(self, file_name):
        try:
            riff_data = self.get_riff_data()
            self.content["zynseq_riff_b64"] = base64.encodebytes(
                riff_data).decode("utf-8").replace('\n', '')
            fpath = PATH_DATA + '/zss/' + file_name + '.zss'
            if exists(fpath):
                fpath = splitext(fpath)[0] + '_new.zss'

            with open(fpath, "w") as fh:
                data = JSONEncoder().encode(self.content)
                fh.write(data)

        except Exception as e:
            logger.error("Can't write snapshot '%s': %s" % (file_name, e))
            return False
