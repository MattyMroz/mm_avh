from os import path, listdir, chdir, getcwd
from typing import List
from rich.console import Console
from utils.execution_timer import execution_timer
from data.settings import Settings
from modules.mkv_tool_nix import MkvToolNix
from natsort import natsorted
from msvcrt import getch


WORKING_SPACE = path.join(getcwd(), 'working_space')
WORKING_SPACE_OUTPUT = path.join(WORKING_SPACE, 'output')
WORKING_SPACE_TEMP = path.join(WORKING_SPACE, 'temp')

console: Console = Console()
@execution_timer
def main():
    """
    Main function :D
    """
    console.print('╚═══ Multimedia Magic – Audio Visual Heaven ═══╝\n', style='bold white')

    console.print('Czy chcesz zmienić ustawienia? (T lub Y - tak):', style='bold green', end=' ')
    if input().lower() in ('t', 'y'):
        chdir(path.dirname('./data/'))
        Settings.change_settings_save_to_file('settings.json')
        chdir(path.dirname('../'))

    path.dirname('./modules/')

    files = listdir(WORKING_SPACE)
    sorted_files = natsorted(files)
    for filename in sorted_files:
        if filename.endswith('.mkv'):
            mkv_tool_nix = MkvToolNix(filename=filename,
                                      working_space=WORKING_SPACE,
                                      working_space_output=WORKING_SPACE_OUTPUT,
                                      working_space_temp=WORKING_SPACE_TEMP)
            mkv_tool_nix.mkv_extract_track(mkv_tool_nix.mkv_info_json())



if __name__ == '__main__':
    main()
    console.print('\n[italic bright_green]Naciśnij dowolny klawisz, aby zakończyć działanie programu...')
    getch()