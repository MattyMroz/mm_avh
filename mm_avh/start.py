from rich.console import Console
from utils.execution_timer import execution_timer
from data.settings import Settings
import os

@execution_timer
def main():
    """
    Main function :D
    """
    console: Console = Console()
    console.print('╚═══ Multimedia Magic – Audio Visual Heaven ═══╝\n', style='bold white')

    console.print('Czy chcesz zmienić ustawienia? (T lub Y - tak):', style='bold green', end=' ')
    if input().lower() in ('t', 'y'):
        os.chdir(os.path.dirname('./data/'))
        Settings.change_settings_save_to_file('settings.json')


if __name__ == '__main__':
    main()

    # x = input('Press any key to exit...')
