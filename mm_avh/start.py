from msvcrt import getch
from natsort import natsorted
from os import path, listdir, chdir, getcwd
from typing import List


from data.settings import Settings

from utils.execution_timer import execution_timer
from utils.number_in_words import NumberInWords
from utils.cool_animation import CoolAnimation

from modules.mkvtoolnix import MkvToolNix
from modules.subtitle import SubtitleRefactor
from modules.translator import SubtitleTranslator
from modules.subtitle_to_speech import SubtitleToSpeech

from constants import (SETTINGS_PATH,
                       WORKING_SPACE,
                       WORKING_SPACE_OUTPUT,
                       WORKING_SPACE_TEMP,
                       WORKING_SPACE_TEMP_MAIN_SUBS,
                       WORKING_SPACE_TEMP_ALT_SUBS,
                       MKV_EXTRACT_PATH,
                       MKV_MERGE_PATH, MKV_INFO_PATH,
                       BALABOLKA_PATH,
                       FFMPEG_PATH,
                       console)


def display_logo():  # ✅
    mm_avh_logo: CoolAnimation = CoolAnimation()
    mm_avh_logo.display()
    console.print(
        '╚═══ Multimedia Magic – Audio Visual Heaven ═══╝\n', style='white_bold')


def ask_user(question: str) -> bool:
    console.print(question, style='bold green', end=' ')
    return input().lower() in ('t', 'y')


def update_settings() -> Settings:  # ✅
    if ask_user('Czy chcesz zmienić ustawienia? (T lub Y - tak):'):
        Settings.change_settings_save_to_file()
        console.print('Zapisano ustawienia.\n', style='green_bold')
    else:
        console.print('Pomijam tę opcję.\n', style='red_bold')
    return Settings.load_from_file()


def extract_tracks_from_mkv():  # ✅
    if ask_user('Czy chcesz wyciągnąć ścieżki z plików mkv? (T lub Y - tak):'):
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
        subtitle.txt_to_srt()


def translate_subtitles(settings):  # ❌
    files_to_translate = {}

    main_subs_files: List[str] = [
        filename for filename in listdir(WORKING_SPACE_TEMP_MAIN_SUBS)
        if path.isfile(path.join(WORKING_SPACE_TEMP_MAIN_SUBS, filename)) and filename.endswith('.srt')
    ]

    main_subs_files = sorted(main_subs_files)

    console.print('TŁUMACZENIE PLIKÓW', style='yellow_bold')
    files_to_translate = {}
    for filename in main_subs_files:
        console.print(
            "Czy chcesz przetłumaczyć plik?", style='green_bold')
        console.print(filename)
        console.print("(T lub Y - tak):", style='green_bold', end=' ')
        if input().lower() in ('t', 'y'):
            files_to_translate[filename] = True
        else:
            console.print('Pomijam tę opcję.\n', style='red_bold')
            files_to_translate[filename] = False

    translator_instance = SubtitleTranslator()

    for filename, should_translate in files_to_translate.items():
        if should_translate:
            translator_instance.translate_srt(filename,
                                              WORKING_SPACE_TEMP_MAIN_SUBS,
                                              settings)
            if path.exists(path.join(WORKING_SPACE_TEMP_ALT_SUBS, filename)):
                translator_instance.translate_srt(filename,
                                                  WORKING_SPACE_TEMP_ALT_SUBS,
                                                  settings)

# def translate_subtitles():  # ❌
#     settings: Settings = Settings.load_from_file('./data/settings.json')

#     main_subs_folder: str = path.join(WORKING_SPACE_TEMP, 'main_subs')
#     alt_subs_folder: str = path.join(WORKING_SPACE_TEMP, 'alt_subs')

#     files_to_translate = {}

#     main_subs_files: List[str] = [
#         filename for filename in listdir(main_subs_folder)
#         if path.isfile(path.join(main_subs_folder, filename)) and filename.endswith('.srt')
#     ]

#     main_subs_files = sorted(main_subs_files)

#     console.print('TŁUMACZENIE PLIKÓW', style='yellow_bold')
#     files_to_translate = {}
#     for filename in main_subs_files:
#         console.print(
#             "Czy chcesz przetłumaczyć plik?", style='green_bold')
#         console.print(filename)
#         console.print("(T lub Y - tak):", style='green_bold', end=' ')
#         if input().lower() in ('t', 'y'):
#             files_to_translate[filename] = True
#         else:
#             console.print('Pomijam tę opcję.\n', style='red_bold')
#             files_to_translate[filename] = False

#     translator_instance = SubtitleTranslator()

#     for filename, should_translate in files_to_translate.items():
#         if should_translate:
#             translator_instance.translate_srt(filename=filename,
#                                               dir_path=main_subs_folder,
#                                               settings=settings)
#             if path.exists(path.join(alt_subs_folder, filename)):
#                 translator_instance.translate_srt(filename=filename,
#                                                   dir_path=alt_subs_folder,
#                                                   settings=settings)


def convert_numbers_to_words():  # ❌
    console.print(
        '\nLICZBY NA SŁOWA - (BEZ POPRAWNOŚCI GRAMATYCZNEJ)', style='bold bright_yellow')
    console.print('Czy chcesz przekonwertować liczby na słowa w tekście? (T lub Y - tak):',
                  style='bold green', end=' ')
    if input().lower() in ('t', 'y'):
        main_subs_folder: str = path.join(WORKING_SPACE_TEMP, 'main_subs')
        srt_files: List[str] = [
            file for file in listdir(main_subs_folder)
            if path.isfile(path.join(main_subs_folder, file)) and file.endswith('.srt')
        ]

        for filename in srt_files:
            subtitle: SubtitleRefactor = SubtitleRefactor(filename=filename,
                                                          working_space=WORKING_SPACE,
                                                          working_space_output=WORKING_SPACE_OUTPUT,
                                                          working_space_temp=WORKING_SPACE_TEMP)
            subtitle.convert_numbers_in_srt('main_subs')
    else:
        console.print('Pomijam tę opcję.\n', style='red_bold')


def generate_audio_for_subtitles():  # ❌
    console.print('\nCzy chcesz generować audio dla napisów? (T lub Y - tak):',
                  style='bold green', end=' ')


@execution_timer  # ❌
def main():
    display_logo()
    settings: Settings = update_settings()
    extract_tracks_from_mkv()
    refactor_subtitles()
    translate_subtitles(settings)
    convert_numbers_to_words()
    generate_audio_for_subtitles(settings)
    subtitle_refactor = SubtitleRefactor(filename='1.srt')
    subtitle_refactor.srt_to_ass()


if __name__ == '__main__':  # ❌
    main()
    console.print(
        '\n[italic bright_green]Naciśnij dowolny klawisz, aby zakończyć działanie programu...', end='')
    getch()
