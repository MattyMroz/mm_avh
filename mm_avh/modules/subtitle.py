from subprocess import Popen, PIPE, CalledProcessError
from json import loads
from typing import List
from os import path
from dataclasses import dataclass
from rich.theme import Theme
from rich.console import Console
from pysubs2 import SSAFile
from pysubs2 import SSAFile
from pyasstosrt import Subtitle


@dataclass(slots=True)
class SubtitleRefactor:
    filename: str  # Nazwa pliku
    working_space: str  # Katalog roboczy
    working_space_output: str  # Katalog wynikowy
    working_space_temp: str  # Katalog tymczasowy

    console: Console = Console(theme=Theme({"repr.number": "bold red"}))  # Konsola z motywem wyglądu

    # Metoda do dzielenia pliku ASS na dwa pliki z wybranymi stylami
    def split_ass(self, input_file: str) -> None:
        main_subs_folder = path.join(self.working_space_temp, 'main_subs')
        alt_subs_folder = path.join(self.working_space_temp, 'alt_subs')

        # Otwarcie pliku ASS i wczytanie napisów
        with open(path.join(self.working_space_temp, input_file), 'r', encoding='utf-8') as file:
            subs = SSAFile.from_file(file)

        # Znalezienie unikalnych stylów w kolejności występowania
        styles = []
        for event in subs:
            if event.style not in styles:
                styles.append(event.style)

        self.console.print("PODZIAŁ PLIKU:", style='bold red')
        self.console.print(input_file, style='bold white')
        self.console.print("Dostępne style do TTS:", style='bold yellow')
        for i, style in enumerate(styles, start=1):
            self.console.print(f"{i}. {style}")

        selected_styles = []
        while True:
            self.console.print("Wybierz style do zapisu (naciśnij ENTER, aby zakończyć): ",
                               style='bold green', end='')
            selection = input("")
            if not selection:
                break
            selected_styles.append(styles[int(selection) - 1])

        if not selected_styles:
            self.console.print("Nie wybrano żadnych stylów. Podział napisów nie został wykonany.\n",
                               style='bold red')
            return

        main_subs = SSAFile()
        alt_subs = SSAFile()

        for event in subs:
            if event.style in selected_styles:
                main_subs.append(event)
            else:
                alt_subs.append(event)

        main_output_file = path.join(main_subs_folder, input_file)
        alt_output_file = path.join(alt_subs_folder, input_file)

        # Skopiowanie metadanych do plików wyjściowych
        main_subs.info = subs.info
        alt_subs.info = subs.info

        # Skopiowanie stylów do plików wyjściowych
        main_style_names = [style_name for style_name in subs.styles.keys()
                            if style_name in selected_styles]
        main_subs.styles.clear()
        for style_name in main_style_names:
            main_subs.styles[style_name] = subs.styles[style_name]

        alt_style_names = [style_name for style_name in subs.styles.keys()
                           if style_name not in selected_styles]
        alt_subs.styles.clear()
        for style_name in alt_style_names:
            alt_subs.styles[style_name] = subs.styles[style_name]

        # Zapis napisów w plikach wyjściowych
        with open(main_output_file, 'w', encoding='utf-8') as main_file:
            main_file.write(main_subs.to_string(format_='ass'))

        with open(alt_output_file, 'w', encoding='utf-8') as alt_file:
            alt_file.write(alt_subs.to_string(format_='ass'))

        self.console.print("Podział napisów został zakończony.", style='bold yellow')

        path.remove(path.join(self.working_space_temp, input_file))
        self.console.print("Usunięto plik źródłowy.\n", style='bold yellow')

    # Metoda do konwersji pliku ASS na SRT
    def ass_to_srt(self, file: str) -> None:
        sub = Subtitle(path.join(self.working_space_temp, file))
        sub.export()
        self.console.print("Zamieniono na srt:", style='bold yellow', end=" ")
        self.console.print(file)

        # path.remove(path.join(self.working_space, file))
        # self.console.print("Usunięto plik źródłowy.", style='bold green')

    # Metoda do zmiany kodowania pliku na ANSI
    def asnii_srt(self, file: str) -> None:
        with open(path.join(self.working_space_temp, file), "r", encoding="utf-8") as source_file:
            content = source_file.read()

        try:
            with open(path.join(self.working_space_temp, file), "w", encoding="ANSI") as target_file:
                target_file.write(content)
        except UnicodeEncodeError:
            with open(path.join(self.working_space_temp, file), "w", encoding="ANSI", errors="ignore") as target_file:
                target_file.write(content)

        self.console.print("Zamieniono kodowanie na ANSI:", style='bold yellow', end=' ')
        self.console.print(file)





# def split_ass(dir_path, input_file):
#     main_subs_folder = os.path.join(dir_path, 'main_subs')
#     alt_subs_folder = os.path.join(dir_path, 'alt_subs')

#     with open(os.path.join(dir_path, input_file), 'r', encoding='utf-8') as file:
#         subs = SSAFile.from_file(file)

#     # Znajdź unikalne style w kolejności występowania
#     styles = []
#     for event in subs:
#         if event.style not in styles:
#             styles.append(event.style)

#     cprint("PODZIAŁ PLIKU: ", 'red', attrs=['bold'])
#     cprint(input_file, 'white', attrs=['bold'])
#     # Wyświetl dostępne style w kolejności występowania
#     cprint("Dostępne style do TTS:", 'yellow', attrs=['bold'])
#     for i, style in enumerate(styles, start=1):
#         print(f"{i}. {style}")

#     print('')
#     selected_styles = []
#     while True:
#         cprint("Wybierz style do zapisu (naciśnij ENTER, aby zakończyć): ",
#                'green', attrs=['bold'], end='')
#         selection = input("")
#         if not selection:
#             break
#         selected_styles.append(styles[int(selection) - 1])

#     if not selected_styles:
#         cprint("Nie wybrano żadnych stylów. Podział napisów nie został wykonany.\n",
#                'red', attrs=['bold'])
#         return

#     main_subs = SSAFile()
#     alt_subs = SSAFile()

#     for event in subs:
#         if event.style in selected_styles:
#             main_subs.append(event)
#         else:
#             alt_subs.append(event)

#     main_output_file = os.path.join(main_subs_folder, input_file)
#     alt_output_file = os.path.join(alt_subs_folder, input_file)

#     # Skopiuj metadane do plików wyjściowych
#     main_subs.info = subs.info
#     alt_subs.info = subs.info

#     # Skopiuj style do plików wyjściowych
#     main_style_names = [style_name for style_name in subs.styles.keys()
#                         if style_name in selected_styles]
#     main_subs.styles.clear()
#     for style_name in main_style_names:
#         main_subs.styles[style_name] = subs.styles[style_name]

#     alt_style_names = [style_name for style_name in subs.styles.keys()
#                        if style_name not in selected_styles]
#     alt_subs.styles.clear()
#     for style_name in alt_style_names:
#         alt_subs.styles[style_name] = subs.styles[style_name]

#     # Zapisz napisy w plikach wyjściowych
#     with open(main_output_file, 'w', encoding='utf-8') as main_file:
#         main_file.write(main_subs.to_string(format_='ass'))

#     with open(alt_output_file, 'w', encoding='utf-8') as alt_file:
#         alt_file.write(alt_subs.to_string(format_='ass'))

#     cprint("Podział napisów został zakończony.", 'yellow', attrs=['bold'])

#     os.remove(os.path.join(dir_path, input_file))
#     cprint("Usunięto plik źródłowy.\n", 'yellow', attrs=['bold'])


# def ass_to_srt(dir_path, file):
#     sub = Subtitle(os.path.join(dir_path, file))
#     sub.export()
#     cprint("Zamieniono na srt:", 'yellow', attrs=['bold'], end=" ")
#     print(file)

#     # os.remove(os.path.join(dir_path, file))
#     # cprint("Usunięto plik źródłowy.", 'green', attrs=['bold'])


# def asnii_srt(dir_path, file):
#     with open(os.path.join(dir_path, file), "r", encoding="utf-8") as source_file:
#         content = source_file.read()

#     try:
#         with open(os.path.join(dir_path, file), "w", encoding="ANSI") as target_file:
#             target_file.write(content)
#     except UnicodeEncodeError:
#         with open(os.path.join(dir_path, file), "w", encoding="ANSI", errors="ignore") as target_file:
#             target_file.write(content)

#     # Zamieniono kodowanie pliku na ANSI
#     cprint("Zamieniono kodowanie na ANSI:", 'yellow', attrs=['bold'], end=' ')
#     print(file)