from os import path, listdir, chdir, getcwd
from typing import List
from rich.theme import Theme
from rich.console import Console
from natsort import natsorted
from msvcrt import getch
from pysubs2 import load

from data.settings import Settings

from utils.execution_timer import execution_timer
from utils.number_in_words import NumberInWords
from utils.cool_animation import CoolAnimation

from modules.mkvtoolnix import MkvToolNix
from modules.subtitle import SubtitleRefactor
from modules.translator import SubtitleTranslator
from modules.subtitle_to_speech import SubtitleToSpeech

from constants import (WORKING_SPACE,
                       WORKING_SPACE_OUTPUT,
                       WORKING_SPACE_TEMP,
                       WORKING_SPACE_TEMP_MAIN_SUBS,
                       WORKING_SPACE_TEMP_ALT_SUBS,
                       MKV_EXTRACT_PATH,
                       MKV_MERGE_PATH, MKV_INFO_PATH,
                       BALABOLKA_PATH,
                       FFMPEG_PATH,
                       console)


@execution_timer
def main():
    """
    Main function :D
    """
    mm_avh_logo: CoolAnimation = CoolAnimation()
    mm_avh_logo.display()
    console.print(
        '╚═══ Multimedia Magic – Audio Visual Heaven ═══╝\n', style='bold white')

    console.print('Czy chcesz zmienić ustawienia? (T lub Y - tak):',
                  style='bright_green_bold', end=' ')
    if input().lower() in ('t', 'y'):
        Settings.change_settings_save_to_file('./data/settings.json')
        console.print('Zapisano ustawienia.\n', style='bold green')
    else:
        console.print('Pomijam tę opcję.\n', style='bold red')
    # path.dirname('./modules/')

    # Extracting tracks from MKV files
    files: List[str] = [file for file in listdir(WORKING_SPACE)
                        if path.isfile(path.join(WORKING_SPACE, file)) and file.endswith('.mkv')]
    sorted_files: List[str] = natsorted(files)
    for filename in sorted_files:
        mkv: MkvToolNix = MkvToolNix(filename=filename,
                                     working_space=WORKING_SPACE,
                                     working_space_output=WORKING_SPACE_OUTPUT,
                                     working_space_temp=WORKING_SPACE_TEMP)
        mkv.mkv_extract_track(mkv.get_mkv_info())

    # Refactoring subtitles
    subtitle_extensions: List[str] = [
        '.sup', '.txt', '.ogg',
        '.ssa', '.ass', '.srt',
        '.sub', '.usf', '.vtt',
    ]

    files: List[str] = [
        file for file in listdir(WORKING_SPACE_TEMP)
        if (
            path.isfile(path.join(WORKING_SPACE_TEMP, file)) and
            any(file.endswith(ext) for ext in subtitle_extensions)
        )
    ]

    sorted_files = natsorted(files)
    for filename in sorted_files:
        subtitle: SubtitleRefactor = SubtitleRefactor(filename=filename,
                                                      working_space=WORKING_SPACE,
                                                      working_space_output=WORKING_SPACE_OUTPUT,
                                                      working_space_temp=WORKING_SPACE_TEMP)
        if filename.endswith('.ass') or filename.endswith('.ssa'):
            subtitle.split_ass('main_subs', 'alt_subs')
            subtitle.ass_to_srt('main_subs', 'alt_subs')
        if filename.endswith('.srt'):
            subtitle.move_srt('main_subs')
        if filename.endswith('.txt'):
            subtitle.txt_to_srt()

    # Translating subtitles
    settings: Settings = Settings.load_from_file('./data/settings.json')

    main_subs_folder: str = path.join(WORKING_SPACE_TEMP, 'main_subs')
    alt_subs_folder: str = path.join(WORKING_SPACE_TEMP, 'alt_subs')

    files_to_translate = {}

    main_subs_files: List[str] = [
        filename for filename in listdir(main_subs_folder)
        if path.isfile(path.join(main_subs_folder, filename)) and filename.endswith('.srt')
    ]

    main_subs_files = sorted(main_subs_files)

    console.print('TŁUMACZENIE PLIKÓW', style='bold bright_yellow')
    files_to_translate = {}
    for filename in main_subs_files:
        console.print(
            "Czy chcesz przetłumaczyć plik?", style='bold green')
        console.print(filename)
        console.print("(T lub Y - tak):", style='bold green', end=' ')
        if input().lower() in ('t', 'y'):
            files_to_translate[filename] = True
        else:
            console.print('Pomijam tę opcję.', style='bold red')
            files_to_translate[filename] = False

    translator_instance = SubtitleTranslator()

    for filename, should_translate in files_to_translate.items():
        if should_translate:
            translator_instance.translate_srt(filename=filename,
                                              dir_path=main_subs_folder,
                                              settings=settings)
            if path.exists(path.join(alt_subs_folder, filename)):
                translator_instance.translate_srt(filename=filename,
                                                  dir_path=alt_subs_folder,
                                                  settings=settings)

    # Zamiana liczb na słowa
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
        console.print('Pomijam tę opcję.', style='bold red')

    # Generowanie audio dla napisów
    console.print('\nCzy chcesz generować audio dla napisów? (T lub Y - tak):',
                  style='bold green', end=' ')


if __name__ == '__main__':
    main()
    console.print(
        '\n[italic bright_green]Naciśnij dowolny klawisz, aby zakończyć działanie programu...', end='')
    getch()
