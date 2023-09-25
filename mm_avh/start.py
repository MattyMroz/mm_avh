from msvcrt import getch
from natsort import natsorted
from os import listdir, makedirs, path
from shutil import rmtree
from typing import Dict, List

from constants import (SETTINGS_PATH,
                       WORKING_SPACE,
                       WORKING_SPACE_OUTPUT,
                       WORKING_SPACE_TEMP,
                       WORKING_SPACE_TEMP_MAIN_SUBS,
                       WORKING_SPACE_TEMP_ALT_SUBS,
                       MKV_EXTRACT_PATH,
                       MKV_MERGE_PATH,
                       MKV_INFO_PATH,
                       BALABOLKA_PATH,
                       FFMPEG_PATH,
                       console)

from data.settings import Settings

from modules.mkvtoolnix import MkvToolNix
from modules.subtitle import SubtitleRefactor
from modules.subtitle_to_speech import SubtitleToSpeech
from modules.translator import SubtitleTranslator
from modules.mkv_processing import MKVProcessing

from utils.cool_animation import CoolAnimation
from utils.execution_timer import execution_timer
from utils.number_in_words import NumberInWords


def display_logo():  # ✅
    mm_avh_logo: CoolAnimation = CoolAnimation()
    mm_avh_logo.display()
    console.print(
        '╚═══ Multimedia Magic – Audio Visual Heaven ═══╝\n', style='white_bold')


def ask_user(question: str) -> bool:
    console.print(question, style='bold green', end=' ')
    return input().lower() in ('t', 'y')


def update_settings() -> Settings:  # ✅
    if ask_user('💾 Czy chcesz zmienić ustawienia? (T lub Y - tak):'):
        Settings.change_settings_save_to_file()
        console.print('Zapisano ustawienia.\n', style='green_bold')
    else:
        console.print('Pomijam tę opcję.\n', style='red_bold')
    return Settings.load_from_file()


def extract_tracks_from_mkv():  # ✅
    if ask_user('🧲 Czy chcesz wyciągnąć ścieżki z plików mkv? (T lub Y - tak):'):
        files: List[str] = get_mkv_files(WORKING_SPACE)
        sorted_files: List[str] = natsorted(files)
        for filename in sorted_files:
            mkv: MkvToolNix = MkvToolNix(filename)
            mkv.mkv_extract_track(mkv.get_mkv_info())
    else:
        console.print('Pomijam tę opcję.\n', style='red_bold')


def get_mkv_files(directory: str) -> List[str]:
    return [file for file in listdir(directory)
            if path.isfile(path.join(directory, file)) and file.endswith('.mkv')]


def refactor_subtitles():  # ✅
    subtitle_extensions: List[str] = [
        '.sup', '.txt', '.ogg',
        '.ssa', '.ass', '.srt',
        '.sub', '.usf', '.vtt',
    ]

    files: List[str] = get_files_with_extensions(
        WORKING_SPACE_TEMP, subtitle_extensions)
    sorted_files = natsorted(files)
    for filename in sorted_files:
        refactor_subtitle_file(filename)


def get_files_with_extensions(directory: str, extensions: List[str]) -> List[str]:
    return [
        file for file in listdir(directory)
        if (
            path.isfile(path.join(directory, file)) and
            any(file.endswith(ext) for ext in extensions)
        )
    ]


def refactor_subtitle_file(filename: str):
    subtitle: SubtitleRefactor = SubtitleRefactor(filename)
    if filename.endswith('.ass') or filename.endswith('.ssa'):
        subtitle.split_ass()
        subtitle.ass_to_srt()
    if filename.endswith('.srt'):
        subtitle.move_srt()
    if filename.endswith('.txt'):
        subtitle.txt_to_srt(10)


def translate_subtitles(settings: Settings):  # ✅
    if not ask_user('💭 Czy chcesz tłumaczyć pliki napisów? (T lub Y - tak):'):
        console.print('Pomijam tę opcję.\n', style='red_bold')
        return

    main_subs_files = get_srt_files(WORKING_SPACE_TEMP_MAIN_SUBS)
    files_to_translate = ask_to_translate_files(main_subs_files)
    translate_files(files_to_translate, settings)


def get_srt_files(directory: str) -> List[str]:
    return [
        filename for filename in listdir(directory)
        if path.isfile(path.join(directory, filename)) and filename.endswith('.srt')
    ]


def ask_to_translate_files(files: List[str]) -> dict:
    files_to_translate: dict = {}
    for filename in files:
        console.print(f"\nTŁUMACZENIE PLIKU:", style='yellow_bold')
        console.print(filename, style='white_bold')
        if ask_user("Czy chcesz przetłumaczyć (T lub Y - tak):"):
            files_to_translate[filename] = True
        else:
            console.print('Pomijam tę opcję.\n', style='red_bold')
            files_to_translate[filename] = False
    return files_to_translate


def translate_files(files_to_translate: dict, settings: Settings):
    translator_instance: SubtitleTranslator = SubtitleTranslator()
    for filename, should_translate in files_to_translate.items():
        if should_translate:
            translator_instance.translate_srt(filename,
                                              WORKING_SPACE_TEMP_MAIN_SUBS,
                                              settings)
            if path.exists(path.join(WORKING_SPACE_TEMP_ALT_SUBS, filename)):
                translator_instance.translate_srt(filename,
                                                  WORKING_SPACE_TEMP_ALT_SUBS,
                                                  settings)


def convert_numbers_to_words():  # ✅
    if not ask_user('🔢 Czy chcesz przekonwertować liczby na słowa w tekście? (T lub Y - tak):'):
        console.print('Pomijam tę opcję.\n', style='red_bold')
        return

    srt_files = get_srt_files(WORKING_SPACE_TEMP_MAIN_SUBS)
    convert_numbers_in_files(srt_files)


def get_srt_files(directory: str) -> List[str]:
    return [
        file for file in listdir(directory)
        if path.isfile(path.join(directory, file)) and file.endswith('.srt')
    ]


def convert_numbers_in_files(files: List[str]):
    for filename in files:
        console.print(
            f"\nKONWERSJA LICZB (BEZ POPRAWNOŚCI GRAMATYCZNEJ) W PLIKU:", style='yellow_bold')
        console.print(filename, style='white_bold')
        if ask_user("Czy chcesz przekonwertować liczby na słowa w tym pliku? (T lub Y - tak):"):
            subtitle: SubtitleRefactor = SubtitleRefactor(filename)
            subtitle.convert_numbers_in_srt()
        else:
            console.print(f'Pomijam plik {filename}.\n', style='red_bold')


def generate_audio_for_subtitles(settings: Settings) -> None:  # ✅
    if not ask_user('🎤 Czy chcesz generować audio dla napisów? (T lub Y - tak):'):
        console.print('Pomijam tę opcję.\n', style='red_bold')
        return

    main_subs_files: List[str] = get_srt_files(WORKING_SPACE_TEMP_MAIN_SUBS)
    files_to_generate_audio: Dict[str, bool] = ask_to_generate_audio_files(
        main_subs_files)
    generate_audio_files(files_to_generate_audio, settings)


def ask_to_generate_audio_files(files: List[str]) -> Dict[str, bool]:
    files_to_generate_audio: Dict[str, bool] = {}
    for filename in files:
        console.print(f"\nGENEROWANIE AUDIO DLA PLIKU:", style='yellow_bold')
        console.print(filename, style='white_bold')
        if ask_user("Czy chcesz wygenerować audio dla tego pliku? (T lub Y - tak):"):
            files_to_generate_audio[filename] = True
        else:
            console.print('Pomijam tę opcję.', style='red_bold')
            files_to_generate_audio[filename] = False
    return files_to_generate_audio


def generate_audio_files(files_to_generate_audio: Dict[str, bool], settings: Settings) -> None:
    audio_generator: SubtitleToSpeech
    if 'TTS - *Głos* - ElevenLans' in settings.tts:
        audio_generator = SubtitleToSpeech('')
        audio_generator.srt_to_eac3_elevenlabs()
    else:
        for filename, should_generate_audio in files_to_generate_audio.items():
            if should_generate_audio:
                audio_generator = SubtitleToSpeech(filename)
                audio_generator.generate_audio(settings)


def refactor_alt_subtitles():  # ✅
    files: List[str] = get_srt_files(WORKING_SPACE_TEMP_ALT_SUBS)
    sorted_files = natsorted(files)
    for filename in sorted_files:
        subtitle: SubtitleRefactor = SubtitleRefactor(filename)
        subtitle.srt_to_ass()


def process_output_files(settings: Settings):
    files = listdir(WORKING_SPACE_OUTPUT)
    files_dict = {path.splitext(file)[0]: [] for file in files}
    for file in files:
        if not file.endswith(('.mkv', '.mp4')):
            files_dict[path.splitext(file)[0]].append(file)

    for base_name, files in files_dict.items():
        if len(files) > 0:
            # https://trac.ffmpeg.org/wiki/Encode/H.264
            # crf_value => 0 ... 18 ... 23 ... 51 ... :(
            # preset_value => 'ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow', 'placebo'
            subtitle_processor = MKVProcessing(filename=base_name,
                                               crf_value='18',
                                               preset_value='medium')
            subtitle_processor.process_mkv(settings)


def clear_temp_folders():
    folders = [WORKING_SPACE_TEMP, WORKING_SPACE_TEMP_MAIN_SUBS,
               WORKING_SPACE_TEMP_ALT_SUBS]
    for folder in folders:
        rmtree(folder, ignore_errors=True)
        makedirs(folder, exist_ok=True)


@execution_timer  # ❌
def main():
    display_logo()
    settings: Settings = update_settings()
    extract_tracks_from_mkv()
    refactor_subtitles()
    translate_subtitles(settings)
    convert_numbers_to_words()
    generate_audio_for_subtitles(settings)
    refactor_alt_subtitles()
    process_output_files(settings)
    clear_temp_folders()


if __name__ == '__main__':  # ❌
    main()
    console.print(
        '\n[green_italic]Naciśnij dowolny klawisz, aby zakończyć działanie programu...', end='')
    getch()
