from dataclasses import dataclass
from os import path, getcwd, pardir, listdir
from rich.console import Console
from rich.theme import Theme
import pyttsx3
import wave
import os
import pysrt
import time
import threading
import subprocess
import asyncio
import contextlib
from pydub import AudioSegment
from edge_tts import Communicate as edge_tts
from typing import Dict


@dataclass(slots=True)
class SubtitleToSpeech:
    filename: str
    working_space: str
    working_space_output: str
    working_space_temp: str

    balabolka_folder: str = path.join(path.abspath(path.join(getcwd(), pardir)),
                                      'mm_avh', 'bin', 'balabolka')
    ffmpeg_folder: str = path.join(path.abspath(path.join(getcwd(), pardir)),
                                   'mm_avh', 'bin', 'ffmpeg', 'bin')

    balabolka_path: str = path.join(balabolka_folder, 'balcon.exe')
    ffmpeg_path: str = path.join(ffmpeg_folder, 'ffmpeg.exe')

    console: Console = Console(theme=Theme({"repr.number": "bold red"}))

    def ansi_srt(self, filename: str) -> None:
        with open(path.join(self.working_space_temp, filename), "r", encoding="utf-8") as source_file:
            content = source_file.read()

        try:
            with open(path.join(self.working_space_temp, filename), "w", encoding="ANSI") as target_file:
                target_file.write(content)
        except UnicodeEncodeError:
            with open(path.join(self.working_space_temp, filename), "w", encoding="ANSI", errors="ignore") as target_file:
                target_file.write(content)

        self.console.print("Zamieniono kodowanie na ANSI:",
                           style='bold bright_yellow', end=' ')
        self.console.print(filename)

    def srt_to_wav_harpo(self, dir_path: str, filename: str, tts_speed: int, tts_volume: float):
        self.ansi_srt(filename)
        # reszta kodu...

    def process_subtitle(self, subtitle: pysrt.SubRipItem):
        i = subtitle.index
        start_time = subtitle.start.to_time().strftime('%H:%M:%S.%f')[:-3]
        end_time = subtitle.end.to_time().strftime('%H:%M:%S.%f')[:-3]
        text = subtitle.text
        print(f"{i}\n{start_time} --> {end_time}\n{text}\n")
        time.sleep(0.02)

    def srt_to_wav_balabolka(self, dir_path: str, tts_path: str, filename: str, tts_speed: int, tts_volume: float):
        self.ansi_srt(filename)
        file_path = os.path.join(tts_path, filename)
        with contextlib.suppress(UnicodeDecodeError):
            subtitles = pysrt.open(file_path, encoding='ANSI')
            balcon_path = self.balabolka_path
            output_wav_path = os.path.join(
                tts_path, os.path.splitext(filename)[0] + ".wav")
        command = f'"{balcon_path}" -fr 48 -f "{file_path}" -w "{output_wav_path}" -n "IVONA 2 Agnieszka" -s {tts_speed} -v {tts_volume}'

        command_thread = threading.Thread(
            target=subprocess.call, args=(command,))

        command_thread.start()

        for i, subtitle in enumerate(subtitles, start=1):
            self.process_subtitle(subtitle)

        command_thread.join()

    async def generate_speech(self, subtitle: pysrt.SubRipItem, voice: str, output_file: str, rate: int, volume: float):
        communicate = edge_tts.Communicate(
            subtitle.text, voice, rate=rate, volume=volume)
        await communicate.save(output_file)

    async def generate_wav_files(self, subtitles: pysrt.SubRipFile, voice: str, rate: int, volume: float):
        tasks = []
        mp3_files = []
        file_name = os.path.splitext(subtitles.path)[0]
        for i, subtitle in enumerate(subtitles, start=1):
            output_file = f"{file_name}_{i}.mp3"
            mp3_files.append(output_file)
            tasks.append(asyncio.create_task(self.generate_speech(
                subtitle, voice, output_file, rate, volume)))
            if i % 50 == 0:
                await asyncio.gather(*tasks)
                tasks = []
                time.sleep(2)
        await asyncio.gather(*tasks)
        return mp3_files

    def merge_audio_files(self, mp3_files: list, subtitles: pysrt.SubRipFile, dir_path: str):
        file_name = os.path.splitext(subtitles.path)[0]
        with wave.open(f"{file_name}.wav", 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(24000)

            audio_segments = []
            for i, mp3_file in enumerate(mp3_files, start=1):
                print(
                    f"{i}\n{subtitles[i-1].start.to_time().strftime('%H:%M:%S.%f')[:-3]} --> {subtitles[i-1].end.to_time().strftime('%H:%M:%S.%f')[:-3]}\n{subtitles[i-1].text}\n")

                mp3_file_path = os.path.join(dir_path, mp3_file)
                if os.path.isfile(mp3_file_path):
                    start_time = subtitles[i-1].start.to_time()
                    start_time = start_time.hour * 3600 + start_time.minute * \
                        60 + start_time.second + start_time.microsecond / 1000000
                    sound = AudioSegment.from_file(mp3_file_path, format="mp3")
                    audio_segments.append(sound)
                    os.remove(mp3_file_path)

                    framerate = wav_file.getframerate()
                    nframes = wav_file.getnframes()
                    current_time = nframes / float(framerate)
                    if current_time < start_time:
                        empty_frame_duration = int(
                            (start_time - current_time) * framerate)
                        empty_frame = b'\x00' * empty_frame_duration * 2
                        wav_file.writeframes(empty_frame)

                    sound_data = sound.raw_data
                    wav_file.writeframes(sound_data)

            wav_file.close()

    def srt_to_wav_edge_online(self, dir_path: str, filename: str, tts: str, tts_speed: int, tts_volume: float):
        self.ansi_srt(filename)
        if tts == "TTS - Zofia - Edge":
            voice = "pl-PL-ZofiaNeural"
        elif tts == "TTS - Marek - Edge":
            voice = "pl-PL-MarekNeural"
        if tts_speed:
            rate = tts_speed
        if tts_volume:
            volume = tts_volume

        subtitles = pysrt.open(os.path.join(
            dir_path, filename), encoding='ANSI')
        mp3_files = asyncio.run(self.generate_wav_files(
            subtitles, voice, rate, volume))
        self.merge_audio_files(mp3_files, subtitles, dir_path)

    def tts_srt(self, dir_path: str, tts_path: str, filename: str, settings: Dict):
        tts = settings.tts
        tts_speed = settings.tts_speed
        tts_volume = settings.tts_volume

        self.console.print(
            "Rozpoczynam generowanie pliku audio... :",
            style='bold yellow', end=' ')
        self.console.print(filename)
        if tts == "TTS - Zosia - Harpo":
            self.srt_to_wav_harpo(tts_path, filename, tts_speed, tts_volume)
        elif tts == "TTS - Agnieszka - Ivona":
            self.srt_to_wav_balabolka(
                dir_path, tts_path, filename, tts_speed, tts_volume)
        elif tts in ["TTS - Zofia - Edge", "TTS - Marek - Edge"]:
            self.srt_to_wav_edge_online(
                tts_path, filename, tts, tts_speed, tts_volume)
        self.console.print(
            "\nGenerowanie pliku audio zakończone.", style='bold yellow')

    def merge_tts_audio(self, tmp_path: str, main_subs_path: str, lector_path: str):
        ffmpeg_path = self.ffmpeg_path
        excluded_extensions = ["srt", "ass"]

        main_subs_files = [f.lower() for f in listdir(main_subs_path)]
        tmp_files = [f.lower() for f in listdir(tmp_path)]

        for file in listdir(tmp_path):
            file_name, file_ext = path.splitext(file)
            file_ext = file_ext[1:].lower()

            if file_ext not in excluded_extensions:
                main_subs_file_path = path.join(
                    lector_path, file)  # zmienione na lector_path
                # zmienione na main_subs_path
                tmp_file_path = path.join(main_subs_path, file)
                output_file = path.join(lector_path, file_name + ".eac3")
                print("Main", main_subs_file_path)
                print("Temp", tmp_file_path)
                print("Output", output_file)
                if file.lower() in main_subs_files and file.lower() in tmp_files:
                    # Jeśli plik istnieje zarówno w main_subs_files, jak i w tmp_files, łączymy je za pomocą ffmpeg
                    command = [
                        ffmpeg_path,
                        "-i", tmp_file_path,
                        "-i", main_subs_file_path,
                        "-filter_complex", "[1:a]volume=7dB[a1];[0:a][a1]amix=inputs=2:duration=first",
                        output_file
                    ]
                    subprocess.call(command)
                    print(f"Zapisano plik: {output_file}")
                else:
                    # Jeśli plik nie istnieje w main_subs, przekonwertuj go na .eac3 za pomocą ffmpeg
                    command = [
                        ffmpeg_path,
                        "-i", tmp_file_path,
                        "-c:a", "eac3",
                        output_file
                    ]
                    subprocess.call(command)
                    print(f"Przekonwertowano plik na .eac3: {output_file}")

                # Usuwamy pliki o tej samej nazwie z main_subs i temp
                if os.path.exists(main_subs_file_path):
                    os.remove(main_subs_file_path)
                if os.path.exists(tmp_file_path):
                    os.remove(tmp_file_path)

    def generate_audio(self, settings: Dict):
        self.tts_srt(self.working_space, self.working_space_temp,
                     self.filename, settings)
        self.merge_tts_audio(self.working_space, self.working_space_temp,
                             self.working_space_output)
