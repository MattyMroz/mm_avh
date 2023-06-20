from subprocess import Popen, PIPE
import json
from typing import List
from os import path, pardir, getcwd
from rich.theme import Theme
from dataclasses import dataclass
from rich.console import Console


@dataclass(slots=True)
class MkvToolNix:
    filename: str
    working_space: str
    working_space_output: str
    working_space_temp: str

    parent_folder: str = path.abspath(path.join(getcwd(), pardir))
    mkv_extract: str = path.join(parent_folder, 'mm_avh', 'bin', 'mkvtoolnix', 'mkvextract.exe')
    mkv_merge: str = path.join(parent_folder, 'mm_avh', 'bin', 'mkvtoolnix', 'mkvmerge.exe')
    mkv_info: str = path.join(parent_folder, 'mm_avh', 'bin', 'mkvtoolnix', 'mkvinfo.exe')

    console: Console = Console(theme=Theme({"repr.number": "bold red"}))

    def mkv_info_json(self):
        command: List[str] = [
            self.mkv_merge,
            '--ui-language',
            'en',
            '--identify',
            '--identification-format',
            'json',
            path.join(self.working_space, self.filename)
        ]

        process: Popen = Popen(
            command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        output, error = map(str.strip, process.communicate())

        if process.returncode == 0:
            return self.mkv_info_print(output)
        else:
            print(f'Error: {error}')

    def mkv_info_print(self, output: str) -> dict:
        data: dict = json.loads(output)
        tracks_data: List[dict] = []

        for track in data['tracks']:
            track_data = {
                'id': track['id'],
                'type': track['type'],
                'codec_id': track['properties']['codec_id'],
                'language': track['properties']['language'],
                'language_ietf': track['properties']['language_ietf'],
                'properties': None
            }

            if 'display_dimensions' in track['properties']:
                track_data['properties'] = track['properties']['display_dimensions']
            elif 'audio_sampling_frequency' in track['properties']:
                track_data['properties'] = f"{track['properties']['audio_sampling_frequency']} Hz"

            tracks_data.append(track_data)

        self.console.print('WYODRĘBNIANIE Z PLIKU:', style='bold bright_yellow')
        self.console.print(self.filename, style='bold white')
        self.console.print('ID  TYPE        CODEK                LANG  LANG_IETF  PROPERTIES',
                           style='bold yellow')

        sorted_tracks = sorted(tracks_data, key=lambda x: x['id'])
        for track in sorted_tracks:
            self.console.print(
                f'[bold bright_yellow]{track["id"]:2}[/bold bright_yellow]  '
                f'[not bold default]{track["type"]:10}  '
                f'{track["codec_id"]:20} '
                f'{track["language"]:5} '
                f'{track["language_ietf"]:10} '
                f'{track["properties"]}'
            )
        print('')
        return data

    def mkv_extract_track(self, data: dict):

        tracks_to_extract: List[int] = []
        while True:
            try:
                self.console.print('Podaj ID ścieżki do wyciągnięcia (naciśnij ENTER, aby zakończyć): ',
                                   style='bold green', end='')
                track_id = int(input(''))
                tracks_to_extract.append(track_id)
            except ValueError:
                self.console.print('Pominięto wyciąganie ścieżki.\n', style='bold red')
                break

        format_dict = {
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

        for track_id in tracks_to_extract:
            track = data['tracks'][track_id]
            codec_id = track['properties']['codec_id']
            format_extension = format_dict.get(codec_id, 'mkv')
            filename = f'{self.filename[:-4]}.{format_extension}'
            out_file = path.join(self.working_space_temp, filename)
            command: List[str] = [
                self.mkv_extract,
                'tracks',
                path.join(self.working_space, self.filename),
                f'{track_id}:{out_file}'
            ]
            process: Popen = Popen(command)
            self.console.print(
                f'Ekstrakcja ścieżki {track_id} do pliku {filename}', style='bold bright_yellow')
            process.wait()

            if process.returncode == 0:
                self.console.print('Ekstrakcja zakończona pomyślnie.\n', style='bold green')
            else:
                self.console.print('Wystąpił błąd podczas ekstrakcji.\n', style='bold red')
