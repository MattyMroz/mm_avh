from rich.console import Console
from utils.execution_timer import execution_timer


@execution_timer
def main():
    """
    Main function :D
    """
    console: Console = Console()
    console.print('╚═══ Multimedia Magic – Audio Visual Heaven ═══╝\n', style='bold white')


if __name__ == '__main__':
    main()
    x = input('Press any key to exit...')
