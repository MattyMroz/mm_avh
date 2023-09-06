import contextlib
from subprocess import Popen, PIPE, CalledProcessError
from json import loads
from typing import List
from os import path, remove, makedirs, rename
from dataclasses import dataclass
from rich.theme import Theme
from rich.console import Console
from pysubs2 import SSAFile, SSAEvent, load
from pyasstosrt import Subtitle
from shutil import move
from nltk.tokenize import sent_tokenize
from utils.number_in_words import NumberInWords


@dataclass(slots=True)
class SubtitleRefactor:
    """
        The SubtitleRefactor class is used for manipulating subtitle files. It provides functionalities such as splitting ASS subtitle files based on styles, converting ASS subtitles to SRT format, and moving SRT files to a specified directory.

        Attributes:
        - filename: The name of the subtitle file to be processed.
        - working_space: The directory where the subtitle file is located.
        - working_space_output: The directory where the output files will be saved.
        - working_space_temp: The directory where temporary files will be saved during processing.
        - console: A Console object from the rich library for pretty printing.
    """
    filename: str
    working_space: str
    working_space_output: str
    working_space_temp: str

    console: Console = Console(theme=Theme({"repr.number": "bold red"}))

    def split_ass(self, main_subs_folder: str, alt_subs_folder: str) -> None:
        """
            Splits an ASS subtitle file into two files based on selected styles.

            Args:
            - main_subs_folder: The directory where the main subtitle file will be saved.
            - alt_subs_folder: The directory where the alternative subtitle file will be saved.
        """
        main_subs_folder: str = path.join(
            self.working_space_temp, main_subs_folder)
        alt_subs_folder: str = path.join(
            self.working_space_temp, alt_subs_folder)

        if not path.exists(main_subs_folder):
            makedirs(main_subs_folder, exist_ok=True)
        if not path.exists(alt_subs_folder):
            makedirs(alt_subs_folder, exist_ok=True)

        with open(path.join(self.working_space_temp, self.filename), 'r', encoding='utf-8') as file:
            subs: SSAFile = SSAFile.from_file(file)

        styles: List[str] = []
        for event in subs:
            if event.style not in styles:
                styles.append(event.style)

        self.console.print("PODZIAŁ PLIKU:", style='bold bright_yellow')
        self.console.print(self.filename, style='bold white')
        self.console.print("Dostępne style do TTS:", style='bold yellow')
        for i, style in enumerate(styles, start=1):
            self.console.print(f"[bold yellow]{i}.[/bold yellow] {style}")

        selected_styles: List[str] = []
        while True:
            self.console.print("Wybierz style do zapisu (naciśnij ENTER, aby zakończyć):",
                               style='bold green', end=" ")
            selection: str = input('')
            if not selection:
                break
            with contextlib.suppress(ValueError):
                selected_index: int = int(selection) - 1
                if 0 <= selected_index < len(styles):
                    selected_styles.append(styles[selected_index])
        if not selected_styles:
            self.console.print("Nie wybrano żadnych stylów. Przeniesiono napisów do main_subs.\n",
                               style='bold green')
            makedirs(main_subs_folder, exist_ok=True)
            alt_file_path: str = path.join(
                self.working_space_temp, self.filename)
            main_file_path: str = path.join(main_subs_folder, self.filename)
            move(alt_file_path, main_file_path)
            return

        main_subs: SSAFile = SSAFile()
        alt_subs: SSAFile = SSAFile()

        for event in subs:
            if event.style in selected_styles:
                main_subs.append(event)
            else:
                alt_subs.append(event)

        main_output_file: str = path.join(main_subs_folder, self.filename)
        alt_output_file: str = path.join(alt_subs_folder, self.filename)

        main_subs.info = subs.info
        alt_subs.info = subs.info

        main_style_names: List[str] = [style_name for style_name in subs.styles.keys()
                                       if style_name in selected_styles]
        main_subs.styles.clear()
        for style_name in main_style_names:
            main_subs.styles[style_name] = subs.styles[style_name]

        alt_style_names: List[str] = [style_name for style_name in subs.styles.keys()
                                      if style_name not in selected_styles]
        alt_subs.styles.clear()
        for style_name in alt_style_names:
            alt_subs.styles[style_name] = subs.styles[style_name]

        with open(main_output_file, 'w', encoding='utf-8') as main_file:
            main_file.write(main_subs.to_string(format_='ass'))

        with open(alt_output_file, 'w', encoding='utf-8') as alt_file:
            alt_file.write(alt_subs.to_string(format_='ass'))

        remove(path.join(self.working_space_temp, self.filename))
        self.console.print("Usunięto plik źródłowy.\n", style='bold yellow')
        self.console.print(
            "Podział napisów zakończony pomyślnie.\n", style='bold green')

    def ass_to_srt(self, *folders) -> None:
        """
            Converts ASS subtitle files to SRT format.

            Args:
            - folders: The directories where the ASS subtitle files are located.
        """
        for folder in folders:
            subs_folder: str = path.join(self.working_space_temp, folder)
            file_path: str = path.join(subs_folder, self.filename)

            if not path.exists(file_path):
                continue

            sub: Subtitle = Subtitle(file_path)
            sub.export()
            self.console.print("Zamieniono na srt:",
                               style='bold green')
            self.console.print(file_path)
        print('')

    def move_srt(self, target_folder: str) -> None:
        """
            Moves an SRT subtitle file to a specified directory.

            Args:
            - target_folder: The directory where the SRT subtitle file will be moved.
        """
        target_subs_folder: str = path.join(
            self.working_space_temp, target_folder)
        target_file_path: str = path.join(target_subs_folder, self.filename)

        if not path.exists(target_subs_folder):
            makedirs(target_subs_folder, exist_ok=True)

        source_file_path: str = path.join(
            self.working_space_temp, self.filename)
        move(source_file_path, target_file_path)
        self.console.print(target_file_path)

    def txt_to_srt(self) -> None:
        """
            Converts a text file to SRT (SubRip Text) format.

            This method reads a text file, tokenizes the text into sentences using the NLTK library, and writes the sentences into a new SRT file. Each sentence becomes a separate subtitle in the SRT file. The original text file is then deleted, and the filename attribute of the class instance is updated to the new SRT file. Finally, the SRT file is moved to the 'main_subs' directory.
        """
        txt_file_path: str = path.join(self.working_space_temp, self.filename)
        srt_file_path: str = txt_file_path.replace('.txt', '.srt')

        with open(txt_file_path, 'r', encoding='utf-8') as file:
            text: str = file.read()

        sentences: List[str] = sent_tokenize(text)

        subs: SSAFile = SSAFile()
        for i, sentence in enumerate(sentences, start=1):
            event: SSAEvent = SSAEvent(start=0, end=0, text=sentence.strip())
            subs.append(event)

        with open(srt_file_path, 'w', encoding='utf-8') as file:
            file.write(subs.to_string(format_='srt'))

        remove(txt_file_path)
        self.console.print(
            f"Przekonwertowano {self.filename} na srt i zapisano:", style='bold green')

        self.filename = self.filename.replace('.txt', '.srt')
        self.move_srt('main_subs')

    def convert_numbers_in_srt(self) -> None:
        """
            Converts numbers in an SRT subtitle file to their word equivalents in Polish.
        """
        srt_file_path: str = path.join(self.working_space_temp, self.filename)

        subs = load(srt_file_path, encoding='utf-8')

        number_in_words = NumberInWords()
        for i, sub in enumerate(subs):
            try:
                sub.text = number_in_words.convert_numbers_in_text(sub.text)
            except IndexError:
                self.console.print(
                    f"[red bold]Wystąpił błąd w napisie {i+1}:[/red bold] {sub.text}.\n[red bold]Pomijam ten napis.")

        subs.save(srt_file_path)

        self.console.print(
            f"Przekonwertowano liczby na słowa w {self.filename}", style='bold green')

    # ! DOTO przenieść do innej klasy
    # Metoda do zmiany kodowania pliku na ANSI
    # def asnii_srt(self, file: str) -> None:
    #     with open(path.join(self.working_space_temp, file), "r", encoding="utf-8") as source_file:
    #         content = source_file.read()

    #     try:
    #         with open(path.join(self.working_space_temp, file), "w", encoding="ANSI") as target_file:
    #             target_file.write(content)
    #     except UnicodeEncodeError:
    #         with open(path.join(self.working_space_temp, file), "w", encoding="ANSI", errors="ignore") as target_file:
    #             target_file.write(content)

    #     self.console.print("Zamieniono kodowanie na ANSI:",
    #                        style='bold yellow', end=' ')
    #     self.console.print(file)


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
