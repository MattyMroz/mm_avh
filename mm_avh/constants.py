from os import getcwd, pardir, path
from rich.console import Console
from rich.style import Style
from rich.theme import Theme

# Path for settings
SETTINGS_PATH: str = path.join(getcwd(), 'data', 'settings.json')

# Main paths
WORKING_SPACE: str = path.join(getcwd(), 'working_space')
WORKING_SPACE_OUTPUT: str = path.join(WORKING_SPACE, 'output')
WORKING_SPACE_TEMP: str = path.join(WORKING_SPACE, 'temp')
WORKING_SPACE_TEMP_MAIN_SUBS: str = path.join(WORKING_SPACE_TEMP, 'main_subs')
WORKING_SPACE_TEMP_ALT_SUBS: str = path.join(WORKING_SPACE_TEMP, 'alt_subs')

# Paths for mkvtoolnix
MKVTOOLNIX_FOLDER: str = path.join(
    path.abspath(path.join(getcwd(), pardir)),
    'mm_avh', 'bin', 'mkvtoolnix'
)
MKV_EXTRACT_PATH: str = path.join(MKVTOOLNIX_FOLDER, 'mkvextract.exe')
MKV_MERGE_PATH: str = path.join(MKVTOOLNIX_FOLDER, 'mkvmerge.exe')
MKV_INFO_PATH: str = path.join(MKVTOOLNIX_FOLDER, 'mkvinfo.exe')

# Paths for balabolka and ffmpeg
BALABOLKA_FOLDER: str = path.join(
    path.abspath(path.join(getcwd(), pardir)),
    'mm_avh', 'bin', 'balabolka'
)
FFMPEG_FOLDER: str = path.join(
    path.abspath(path.join(getcwd(), pardir)),
    'mm_avh', 'bin', 'ffmpeg', 'bin'
)
BALABOLKA_PATH: str = path.join(BALABOLKA_FOLDER, 'balcon.exe')
FFMPEG_PATH: str = path.join(FFMPEG_FOLDER, 'ffmpeg.exe')


# Rich print styles
console: Console = Console(theme=Theme({
    "purple_bold": "purple bold",
    "purple_italic": "purple italic",
    "pink_bold": "rgb(255,105,180) bold",
    "pink_italic": "rgb(255,105,180) italic",
    "red_bold": "rgb(230,0,0) bold",
    "red_italic": "rgb(230,0,0) italic",
    "brown_bold": "rgb(180,82,45) bold",
    "brown_italic": "rgb(180,82,45) italic",
    "orange_bold": "rgb(255,140,0) bold",
    "orange_italic": "rgb(255,140,0) italic",
    "yellow_bold": "rgb(250,237,39) bold",
    "yellow_italic": "rgb(250,237,39) italic",
    "bright_green_bold": "rgb(154,230,50) bold",
    "bright_green_italic": "rgb(154,230,50) italic",
    "green_bold": "rgb(0,150,0) bold",
    "green_italic": "rgb(0,150,0) italic",
    "light_blue_bold": "rgb(160,216,220) bold",
    "light_blue_italic": "rgb(160,216,220) italic",
    "blue_bold": "rgb(0,30,240) bold",
    "blue_italic": "rgb(0,30,240) italic",
    "white_bold": "white bold",
    "white_italic": "white italic",
    "normal_bold": "bold",
    "normal_italic": "italic",
    "black_bold": "rgb(0,0,0) on white bold",
    "black_italic": "rgb(0,0,0) on white italic",
    "repr.number": "bold red",
}))

# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="purple_bold")console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="pan_boll")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="redwn_itold")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="orange_italic")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="yellow_bold")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="yellow_italic")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="bright_green_bold")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="bright_green_italic")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="green_bold")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="green_italic")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="light_blue_bold")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="light_blue_italic")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="blue_bold")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="blue_italic")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="white_bold")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="white_italic")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="normal_bold")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="normal_italic")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="black_bold")
# console.print("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝", style="black_italic")
# input()
