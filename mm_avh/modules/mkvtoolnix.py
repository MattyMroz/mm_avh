from subprocess import Popen, PIPE, CalledProcessError
from json import loads
from typing import Dict, List, Set
from os import getcwd, pardir, path
from dataclasses import dataclass
import sys
from rich.theme import Theme
from rich.console import Console


@dataclass(slots=True)
class MkvToolNix:
    """
        The MkvToolNix class is used for manipulating MKV files. It uses tools from the MKVToolNix package such as mkvextract, mkvmerge, and mkvinfo.

        Attributes:
        filename: The name of the MKV file to be processed.
        working_space: The directory where the MKV file is located.
        working_space_output: The directory where the output files will be saved.
        working_space_temp: The directory where temporary files will be saved during processing.
        mkvtoolnix_folder: The directory where the MKVToolNix tools are located.
        mkv_extract_path: The path to the mkvextract executable.
        mkv_merge_path: The path to the mkvmerge executable.
        mkv_info_path: The path to the mkvinfo executable.
        console: A Console object from the rich library for pretty printing.
    """
    filename: str
    working_space: str
    working_space_output: str
    working_space_temp: str

    mkvtoolnix_folder: str = path.join(path.abspath(path.join(getcwd(), pardir)),
                                       'mm_avh', 'bin', 'mkvtoolnix')
    mkv_extract_path: str = path.join(mkvtoolnix_folder, 'mkvextract.exe')
    mkv_merge_path: str = path.join(mkvtoolnix_folder, 'mkvmerge.exe')
    mkv_info_path: str = path.join(mkvtoolnix_folder, 'mkvinfo.exe')

    console: Console = Console(theme=Theme({"repr.number": "bold red"}))

    def check_executables(self) -> None:
        """
            Checks if the MKVToolNix executables exist at the specified paths.
            If any executable is not found, the program will exit with an error message.
        """
        executables: List[str] = [self.mkv_extract_path,
                                  self.mkv_merge_path, self.mkv_info_path]
        for executable in executables:
            if not path.exists(executable):
                self.console.print(
                    f'Error: {executable} not found', style='bold red')
                sys.exit()

    def get_mkv_info(self) -> dict:
        """
            Retrieves information about the MKV file using the mkvinfo tool.
            The information is returned as a dictionary and also printed to the console.
            If an error occurs during the process, the program will exit with an error message.
        """
        try:
            self.check_executables()
            command: List[str] = self._get_mkv_info_command()
            with Popen(command, stdout=PIPE, stderr=PIPE, universal_newlines=True) as process:
                output, error = process.communicate()

                if process.returncode == 0:
                    data: dict = loads(output)
                    tracks_data: List[dict] = self._parse_tracks_data(data)
                    self._print_mkv_info(tracks_data)
                    return data

                self.console.print(f'Error: {error}', style='bold red')
        except (FileNotFoundError, CalledProcessError) as error:
            self.console.print(f'Error: {error}', style='bold red')
            sys.exit()
        return {}

    def _get_mkv_info_command(self) -> List[str]:
        """
            Constructs the command to be used for retrieving information about the MKV file with mkvinfo.
            Returns the command as a list of strings.
        """
        return [
            self.mkv_merge_path,
            '--ui-language',
            'en',
            '--identify',
            '--identification-format',
            'json',
            path.join(self.working_space, self.filename)
        ]

    def _parse_tracks_data(self, data: dict) -> List[dict]:
        """
            Parses the track data from the dictionary returned by mkvinfo.
            Returns a list of dictionaries, each representing a track in the MKV file.
        """
        tracks_data: List[dict] = []

        for track in data['tracks']:
            track_data: dict = self._parse_track_data(track)
            tracks_data.append(track_data)

        return sorted(tracks_data, key=lambda x: x['id'])

    def _parse_track_data(self, track: dict) -> dict:
        """
            Parses the data for a single track from the dictionary returned by mkvinfo.
            Returns a dictionary with the track's ID, type, codec ID, language, IETF language, and properties.
        """
        properties = track['properties']
        track_data: dict = {
            'id': track['id'],
            'type': track['type'],
            'codec_id': properties.get('codec_id', ''),
            'language': properties['language'],
            'language_ietf': properties['language_ietf'],
            'properties': self._get_track_properties(properties)
        }

        return track_data

    @staticmethod
    def _get_track_properties(properties: dict) -> str:
        """
            Retrieves the properties of a track from the dictionary returned by mkvinfo.
            Returns the properties as a string.
        """
        if 'display_dimensions' in properties:
            return properties['display_dimensions']
        if 'audio_sampling_frequency' in properties:
            return f"{properties['audio_sampling_frequency']} Hz"
        return 'None'

    def _print_mkv_info(self, tracks_data: List[dict]) -> None:
        """
            Prints the information about the MKV file to the console.
            The information includes the ID, type, codec ID, language, IETF language, and properties of each track.
        """
        self.console.print('WYODRĘBNIANIE Z PLIKU:',
                           style='bold bright_yellow')
        self.console.print(self.filename, style='bold white')
        self.console.print('ID  TYPE        CODEK                LANG  LANG_IETF  PROPERTIES',
                           style='bold bright_yellow')

        for track in tracks_data:
            self.console.print(
                f'[bold bright_yellow]{track["id"]:2}[/bold bright_yellow]  '
                f'[not bold default]{track["type"]:10}  '
                f'{track["codec_id"]:20} '
                f'{track["language"]:5} '
                f'{track["language_ietf"]:10} '
                f'{track["properties"]}'
            )
        self.console.print()

    def mkv_extract_track(self, data: Dict[str, any]) -> None:
        """
            Extracts the specified tracks from the MKV file using the mkvextract tool.
            The tracks to be extracted are specified by their IDs.
            The user is prompted to enter the IDs of the tracks to be extracted.
            If an error occurs during the process, the program will exit with an error message.
        """
        valid_track_range: range = range(len(data['tracks']))
        tracks_to_extract: Set[int] = set()

        while True:
            try:
                self.console.print('Podaj ID ścieżki do wyciągnięcia (naciśnij ENTER, aby zakończyć): ',
                                   style='bold green', end='')
                track_input: str = input().strip()
                if not track_input:
                    break
                track_id: int = int(track_input)

                if track_id in valid_track_range:
                    tracks_to_extract.add(track_id)
                else:
                    self.console.print(
                        'Nieprawidłowy ID ścieżki. Proszę podać poprawny numer ścieżki.\n', style='bold red')
            except ValueError:
                self.console.print(
                    'Pominięto wyciąganie ścieżki.\n', style='bold red')

        try:
            for track_id in tracks_to_extract:
                track: str = data['tracks'][track_id]
                codec_id: str = track['properties']['codec_id']
                format_extension: str = self._get_format_extension(codec_id)
                filename: str = f'{self.filename[:-4]}.{format_extension}'
                out_file: str = path.join(self.working_space_temp, filename)
                command: List[str] = self._get_extract_command(
                    track_id, out_file)

                with Popen(command) as process:
                    self.console.print(
                        f'\nEkstrakcja ścieżki {track_id} do pliku {filename}', style='bold bright_yellow')
                    process.wait()

        except (IndexError, KeyError):
            self.console.print(
                'Znaleziono nieprawidłowe ID ścieżki!', style='red bold')
            self.mkv_extract_track(data)

        self.console.print(
            'Ekstrakcja zakończona pomyślnie.\n', style='bold green')

    @staticmethod
    def _get_format_extension(codec_id: str) -> str:
        """
            Determines the file extension for a track based on its codec ID.
            Returns the file extension as a string.
        """
        format_dict: dict = {
            'A_AAC/MPEG2/*': 'aac',
            'A_AAC/MPEG4/*': 'aac',
            'A_AAC': 'aac',
            'A_AC3': 'ac3',
            'A_EAC3': 'ac3',
            'A_ALAC': 'caf',
            'A_DTS': 'dts',
            'A_FLAC': 'flac',
            'A_MPEG/L2': 'mp2',
            'A_MPEG/L3': 'mp3',
            'A_OPUS': 'opus',
            'A_PCM/INT/LIT': 'wav',
            'A_PCM/INT/BIG': 'wav',
            'A_REAL/*': 'rm',
            'A_TRUEHD': 'truehd',
            'A_MLP': 'mlp',
            'A_TTA1': 'tta',
            'A_VORBIS': 'ogg',
            'A_WAVPACK4': 'wv',
            'S_HDMV/PGS': 'sup',
            'S_HDMV/TEXTST': 'txt',
            'S_KATE': 'ogg',
            'S_TEXT/SSA': 'ssa',
            'S_TEXT/ASS': 'ass',
            'S_SSA': 'ssa',
            'S_ASS': 'ass',
            'S_TEXT/UTF8': 'srt',
            'S_TEXT/ASCII': 'srt',
            'S_VOBSUB': 'sub',
            'S_TEXT/USF': 'usf',
            'S_TEXT/WEBVTT': 'vtt',
            'V_MPEG1': 'mpeg',
            'V_MPEG2': 'mpeg',
            'V_MPEG4/ISO/AVC': 'h264',
            'V_MPEG4/ISO/HEVC': 'h265',
            'V_MS/VFW/FOURCC': 'avi',
            'V_REAL/*': 'rm',
            'V_THEORA': 'ogg',
            'V_VP8': 'ivf',
            'V_VP9': 'ivf'
        }

        return format_dict.get(codec_id, 'mkv')

    def _get_extract_command(self, track_id: int, out_file: str) -> List[str]:
        """
            Constructs the command to be used for extracting a track from the MKV file with mkvextract.
            Returns the command as a list of strings.
        """
        return [
            self.mkv_extract_path,
            'tracks',
            path.join(self.working_space, self.filename),
            f'{track_id}:{out_file}'
        ]
