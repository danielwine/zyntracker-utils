import sys
import argparse
import traceback
import pysftp
from os import listdir
import paramiko
from app.io.os import StdOut, get_context, trim_extension
from app.config import (
    PATH_XRNS, PATH_ZSS_REMOTE, SFTP_HOST, SFTP_USER, SFTP_PASSWORD)
from app.shared.xrns import XRNS
from app.audio.sequencer import Sequencer


class Connection(pysftp.Connection):
    def __init__(self):
        super().__init__(host=SFTP_HOST, username=SFTP_USER,
                         password=SFTP_PASSWORD)

    def upload(self, src_path, dest_path, snapshot_folder):
        try:
            self.put(src_path, dest_path, preserve_mtime=True)
        except FileNotFoundError:
            print(f'Bad target "{dest_path}"')
            exit()
        print(f'ZSS uploaded to snapshot folder {snapshot_folder}.')

    def get_remote_file(self, src_path, dest_path):
        if self.exists(src_path):
            self.get(src_path, dest_path)
            return True
        else:
            return False


class App:
    def __init__(self) -> None:
        self.stdout = StdOut()
        self.context = get_context()
        self.seq = Sequencer()
        self.xrns = XRNS()

    def parse_args(self, args=None):
        parser = argparse.ArgumentParser()
        print('XRNS-ZSS bridge by danielwine')
        parser.add_argument('filename', type=str)
        parser.add_argument('--upload', dest='upload_path', metavar="PATH",
                            type=str,
                            help='Specify destination snapshot subfolder')
        parser.add_argument('--debug', action='store_true',
                            help='Switch debug mode on (unhide stdout)')
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

    def connect(self):
        try:
            self.conn = Connection()
            error = f'Your Zynthian cannot be reached at {SFTP_HOST}'
        except pysftp.exceptions.ConnectionException:
            print(f'Timeout. {error}')
            exit()
        except paramiko.ssh_exception.SSHException:
            print(f'No route to host. {error}')
            exit()
        print("Connection to zynthian established.")

    def load(self, file, debug=False):
        try:
            self.xrns.load(file)
        except FileNotFoundError:
            try:
                self.xrns.load(file, standard_path=False)
            except FileNotFoundError:
                self.leave(file)

        if not debug:
            self.stdout.mute()
        self.seq.initialize(self.context['path_lib'], scan=False)
        try:
            self.seq.import_project(file, self.xrns.project)
        except Exception as e:
            self.stdout.unmute()
            print('Unable to import project. An error occured:')
            print(traceback.format_exception_only(e)[0], end='')
            exit()
        self.stdout.unmute()

    def update(self, local_path, remote_path, snapshot_folder=''):
        self.connect()
        if self.conn.get_remote_file(remote_path, local_path):
            print(f'Found project on server. Updating...')
            self.seq.load_snapshot(local_path, load_sequence=False)
        self.seq.save_file(file_path=local_path)
        self.conn.upload(local_path, remote_path, snapshot_folder)
        self.conn.close()

    def print_statistics(self):
        print(f'Project {self.xrns.source.project_name} converted.')
        project = self.xrns.project
        print(f'  total groups: {len(project.get_groups())}')
        print(f'  total sequences: {project.get_total_phrases()}')
        print(f'  transposed sequences: ' +
              f'{project.get_transposable_phrases() * 16}')

    def leave(self, filename):
        print(f'Missing file: {filename}')
        self.list_files()
        exit()

    def run(self):
        p_args = self.parse_args()
        file = p_args.filename
        self.load(file, debug=p_args.debug)
        self.print_statistics()

        local_path = self.xrns.get_original_path() + '.zss'
        remote_path = f'{PATH_ZSS_REMOTE}{p_args.upload_path}'
        remote_path += f'/{trim_extension(local_path.split("/")[-1])}.zss'

        self.seq.save_file(file_path=local_path)
        if remote_path is not None:
            self.update(local_path, remote_path,
                        snapshot_folder=p_args.upload_path)


if __name__ == '__main__':
    app = App()
    app.run()
