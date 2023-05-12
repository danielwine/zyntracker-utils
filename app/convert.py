import sys
import argparse
from os import listdir
from app.io.os import StdOut, get_context, trim_extension
from app.config import PATH_XRNS, SFTP_HOST, SFTP_USER, SFTP_PASSWORD
from app.shared.xrns import XRNS
from app.audio.sequencer import Sequencer


class App:
    def __init__(self) -> None:
        self.stdout = StdOut()
        self.context = get_context()
        self.seq = Sequencer()
        self.xrns = XRNS()

    def parse_args(self, args=None):
        parser = argparse.ArgumentParser()
        print('XRNS-ZSS converter by danielwine')
        parser.add_argument('filename', type=str)
        parser.add_argument('--upload', dest='upload_path', metavar="PATH",
                            type=str,
                            help='Specify destination snapshot subfolder')
        list_info = parser.add_mutually_exclusive_group(required=False)
        list_info.add_argument('--list', action='store_true',
                               help='List')
        if len(sys.argv) == 1:
            print('Parameter "filename" is missing.')
            self.list_files()
            exit()
        return parser.parse_args(args)

    def list_files(self):
        print('Available files in standard path: ')
        files = [file for file in listdir(PATH_XRNS) if
                 file.endswith('.xrns')]
        files.sort()
        for file in files:
            print(' ', file)

    def upload(self, file_path, destination):
        destination += f"/{trim_extension(file_path.split('/')[-1])}.zss"
        import pysftp
        with pysftp.Connection(host=SFTP_HOST, username=SFTP_USER,
                               password=SFTP_PASSWORD) as sftp:
            print("Connection to zynthian established.")
            sftp.cwd('/zynthian/zynthian-my-data/snapshots/')
            try:
                sftp.put(file_path, destination, preserve_mtime=True)
            except FileNotFoundError:
                print(f'Bad target "{destination}"')
                exit()
            print(f'ZSS uploaded to {destination}')

    def leave(self, filename):
        print(f'Missing file: {filename}')
        self.list_files()
        exit()

    def run(self):
        p_args = self.parse_args()
        file = p_args.filename
        upload = p_args.upload_path
        try:
            self.xrns.load(file)
        except FileNotFoundError:
            try:
                self.xrns.load(file, standard_path=False)
            except FileNotFoundError:
                self.leave(file)

        self.stdout.mute()
        self.seq.initialize(self.context['path_lib'], scan=False)
        self.seq.import_project(file, self.xrns.project)
        self.stdout.unmute()
        print(f'Project {self.xrns.source.project_name} converted.')
        project = self.xrns.project
        print(f'  total groups: {len(project.get_groups())}')
        print(f'  total sequences: {project.get_total_phrases()}')
        file_path = self.xrns.get_original_path() + '.zss'
        self.seq.save_file(file_path=file_path)
        if upload is not None:
            self.upload(file_path, upload)


if __name__ == '__main__':
    app = App()
    app.run()
