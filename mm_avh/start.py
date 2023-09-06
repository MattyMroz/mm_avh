from os import path, listdir, chdir, getcwd
from typing import List
from rich.console import Console
from utils.execution_timer import execution_timer
from utils.number_in_words import NumberInWords
from data.settings import Settings
from modules.mkvtoolnix import MkvToolNix
from modules.subtitle import SubtitleRefactor
from natsort import natsorted
from msvcrt import getch
from pysubs2 import load

WORKING_SPACE: str = path.join(getcwd(), 'working_space')
WORKING_SPACE_OUTPUT: str = path.join(WORKING_SPACE, 'output')
WORKING_SPACE_TEMP: str = path.join(WORKING_SPACE, 'temp')

console: Console = Console()


@execution_timer
def main():
    """
    Main function :D
    """
    console.print(
        '╚═══ Multimedia Magic – Audio Visual Heaven ═══╝\n', style='bold white')

    console.print('Czy chcesz zmienić ustawienia? (T lub Y - tak):',
                  style='bold green', end=' ')
    if input().lower() in ('t', 'y'):
        chdir(path.dirname('./data/'))
        Settings.change_settings_save_to_file('settings.json')
        chdir(path.dirname('../'))

    path.dirname('./modules/')

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


    console.print('Czy chcesz przekonwertować liczby na słowa w plikach SRT? (T lub Y - tak):',
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
                                                          working_space_temp=main_subs_folder)
            subtitle.convert_numbers_in_srt()


if __name__ == '__main__':
    main()
    console.print(
        '\n[italic bright_green]Naciśnij dowolny klawisz, aby zakończyć działanie programu...')
    getch()