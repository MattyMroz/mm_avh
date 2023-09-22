import contextlib
from dataclasses import dataclass
from os import path, makedirs
from shutil import move
from typing import List
from constants import (WORKING_SPACE,
                       WORKING_SPACE_OUTPUT,
                       WORKING_SPACE_TEMP,
                       MKV_MERGE_PATH,
                       FFMPEG_PATH,
                       console)
import subprocess
import os
import shutil
from data.settings import Settings
import re


@dataclass
class MKVProcessing:
    filename: str
    working_space: str = WORKING_SPACE
    working_space_output: str = WORKING_SPACE_OUTPUT
    working_space_temp: str = WORKING_SPACE_TEMP
    mkv_merge_path: str = MKV_MERGE_PATH
    ffmpeg_path: str = FFMPEG_PATH

    crf_value: str = '18'
    preset_value: str = 'ultrafast'

    def process_subtitles(self, settings: Settings) -> None:
        options = {
            'Oglądam w MM_AVH_Players (wynik: napisy i audio)': self.move_files_to_working_space,
            'Scal do mkv': self.mkv_merge,
            'Wypal do mp4': self.mkv_burn_to_mp4,
        }

        process_method = options.get(settings.output)
        if process_method:
            process_method()

    def move_files_to_working_space(self) -> None:
        for filename in os.listdir(self.working_space_output):
            if filename.startswith(self.filename):
                shutil.move(os.path.join(self.working_space_output,
                            filename), self.working_space)

    def mkv_merge(self) -> None:
        input_file = os.path.join(self.working_space, self.filename + '.mkv')
        output_file = os.path.join(
            self.working_space_output, self.filename + '.mkv')

        subtitle_file_srt = os.path.join(
            self.working_space_output, self.filename + '.srt')
        subtitle_file_ass = os.path.join(
            self.working_space_output, self.filename + '.ass')
        lector_file = os.path.join(
            self.working_space_output, self.filename + '.eac3')

        # Dodaj ścieżki do pliku bez metadanych
        command = [self.mkv_merge_path, '-o', output_file, input_file]
        if os.path.exists(lector_file):
            command.extend(['--language', '0:pol',
                            '--track-name', '0:Lektor PL',
                            '--default-track', '0:no',
                            lector_file])
        if os.path.exists(subtitle_file_srt):
            command.extend(['--language', '0:pol',
                            '--track-name', '0:Napisy Poboczne PL',
                            '--default-track', '0:no',
                            subtitle_file_srt])
        elif os.path.exists(subtitle_file_ass):
            command.extend(['--language', '0:pol',
                            '--track-name', '0:Napisy Poboczne PL',
                            '--default-track', '0:no',
                            subtitle_file_ass])

        process = subprocess.Popen(command)
        process.communicate()

        if os.path.exists(subtitle_file_srt):
            os.remove(subtitle_file_srt)
        if os.path.exists(subtitle_file_ass):
            os.remove(subtitle_file_ass)
        if os.path.exists(lector_file):
            os.remove(lector_file)

    def mkv_burn_to_mp4(self) -> None:
        filename = self.filename + '.mkv'
        new_filename = re.sub(r'[^A-Za-z0-9.]+', '_', filename)

        os.rename(os.path.join(self.working_space, filename),
                  os.path.join(self.working_space, new_filename))

        subtitle_file_srt = os.path.join(
            self.working_space_output, self.filename + '.srt')
        subtitle_file_ass = os.path.join(
            self.working_space_output, self.filename + '.ass')
        lector_file = os.path.join(
            self.working_space_output, self.filename + '.eac3')

        output_file = os.path.join(
            self.working_space_output, new_filename[:-4] + '.mp4')

        command = []

        if (os.path.exists(subtitle_file_srt) or os.path.exists(subtitle_file_ass)) and os.path.exists(lector_file):
            command = [self.ffmpeg_path, '-y', '-i', os.path.join(
                self.working_space, new_filename), '-i', lector_file.replace("\\", "/")[2:], '-c:v', 'libx264', '-crf', self.crf_value, '-preset', self.preset_value, '-c:a', 'aac', '-map', '0:v:0', '-map', '1:a:0']

            if os.path.exists(subtitle_file_srt):
                command.extend(
                    ['-vf', 'subtitles=' + subtitle_file_srt.replace("\\", "/")[2:]])
            elif os.path.exists(subtitle_file_ass):
                command.extend(
                    ['-vf', 'subtitles=' + subtitle_file_ass.replace("\\", "/")[2:]])

        # Jeśli jest tylko audio
        elif os.path.exists(lector_file):
            command = [self.ffmpeg_path, '-y', '-i', os.path.join(
                self.working_space, new_filename), '-i', lector_file.replace("\\", "/")[2:], '-c:v', 'copy', '-c:a', 'aac', '-map', '0:v:0', '-map', '1:a:0']

        # Jeśli są napisy
        elif os.path.exists(subtitle_file_srt) or os.path.exists(subtitle_file_ass):
            command = [self.ffmpeg_path, '-y', '-i', os.path.join(
                self.working_space, new_filename), '-c:v', 'libx264', '-crf', self.crf_value, '-preset', self.preset_value, '-c:a', 'copy']

            if os.path.exists(subtitle_file_srt):
                command.extend(
                    ['-vf', 'subtitles=' + subtitle_file_srt.replace("\\", "/")[2:]])
            elif os.path.exists(subtitle_file_ass):
                command.extend(
                    ['-vf', 'subtitles=' + subtitle_file_ass.replace("\\", "/")[2:]])

        command.append(output_file.replace("\\", "/")[2:])

        with contextlib.suppress(Exception):
            subprocess.call(command)

        if os.path.exists(output_file):
            os.rename(output_file, os.path.join(
                self.working_space_output, filename[:-4] + '.mp4'))

        os.rename(os.path.join(self.working_space, new_filename),
                  os.path.join(self.working_space, filename))

        if os.path.exists(subtitle_file_srt):
            os.remove(subtitle_file_srt)
        if os.path.exists(subtitle_file_ass):
            os.remove(subtitle_file_ass)
        if os.path.exists(lector_file):
            os.remove(lector_file)
