from rich.console import Console
from utils.execution_timer import execution_timer
from data.config import Config

TRANSLATORS = Config.get_translators()
TRANSLATION_OPTIONS = Config.get_translation_options()
VOICE_ACTORS = Config.get_voice_actors()
OUTPUT = Config.get_output()


@execution_timer
def main():
    """
    Main function :D
    """
    console: Console = Console()
    console.print('╚═══ Multimedia Magic – Audio Visual Heaven ═══╝\n', style='bold white')


if __name__ == '__main__':
    main()
    # x = input('Press any key to exit...')
