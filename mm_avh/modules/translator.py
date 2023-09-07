from dataclasses import dataclass
from typing import Optional
import os
import pysrt
from googletrans import Translator
import deepl
import pyautogui
import pyperclip
import time
import subprocess
from rich.theme import Theme
from rich.console import Console
from data.settings import Settings
# from revChatGPT.V1 import Chatbot


@dataclass(slots=True)
class SubtitleTranslator:
    translator: Optional[str] = None
    deepl_api_key: Optional[str] = None
    translated_line_count: Optional[str] = None

    console: Console = Console(theme=Theme({"repr.number": "bold red"}))

    @staticmethod
    def translate_google(filename, dir_path, translated_line_count):
        subs = pysrt.open(os.path.join(dir_path, filename), encoding='utf-8')
        subs_combined = []
        translated_subs = []

        translator = Translator()
        for i, sub in enumerate(subs):
            sub.text = sub.text.replace("\n", " ◍ ")
            subs_combined.append(sub.text)

            if (i + 1) % translated_line_count == 0 or i == len(subs) - 1:
                combined_text = "\n".join(subs_combined)
                translated_text = translator.translate(
                    combined_text, dest='pl').text
                translated_subs += translated_text.split("\n")
                subs_combined = []

        for i, sub in enumerate(subs):
            sub.text = translated_subs[i]
            sub.text = sub.text.replace(" ◍, ", ",\n")
            sub.text = sub.text.replace(" ◍ ", "\n")
            sub.text = sub.text.replace(" ◍", "")

        subs.save(os.path.join(dir_path, filename))

    @staticmethod
    def translate_deepl_api(filename, dir_path, translated_line_count, deepl_api_key):
        subs = pysrt.open(os.path.join(dir_path, filename), encoding='utf-8')
        translator = deepl.Translator(deepl_api_key)
        groups = [subs[i:i+translated_line_count]
                  for i in range(0, len(subs), translated_line_count)]
        for group in groups:
            text = " @\n".join(sub.text.replace("\n", " ◍◍◍◍ ")
                               for sub in group)
            translated_text = translator.translate_text(
                text, target_lang='PL').text
            translated_texts = translated_text.split(" @\n")
            if len(translated_texts) == len(group):
                for i in range(len(group)):
                    if i < len(translated_texts):
                        group[i].text = translated_texts[i]
                        group[i].text = group[i].text.replace(" ◍◍◍◍, ", ",\n")
                        group[i].text = group[i].text.replace(" ◍◍◍◍ ", "\n")
                        group[i].text = group[i].text.replace(" ◍◍◍◍", "")
        subs.save(os.path.join(dir_path, filename), encoding='utf-8')

    @staticmethod
    def translate_deepl_desktop(filename, dir_path, translated_line_count):
        command = r'C:\Users\mateu\AppData\Roaming\Programs\Zero Install\0install-win.exe'
        args = ["run", "--no-wait",
                "https://appdownload.deepl.com/windows/0install/deepl.xml"]
        subprocess.call([command] + args)

        time.sleep(5)

        def auto_steps():
            screen_width, screen_height = pyautogui.size()
            x = screen_width * 0.25
            y = screen_height * 0.5
            pyautogui.moveTo(x, y)
            pyautogui.click()
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.hotkey('del')
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(6)
            x = screen_width * 0.75
            pyautogui.moveTo(x, y)
            pyautogui.click()
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.hotkey('ctrl', 'c')

        subs = pysrt.open(os.path.join(dir_path, filename), encoding='utf-8')
        groups = [subs[i:i+translated_line_count]
                  for i in range(0, len(subs), translated_line_count)]

        for group in groups:
            text = " @\n".join(sub.text.replace("\n", " ◍◍◍◍ ")
                               for sub in group)
            text = text.rstrip('\n')
            pyperclip.copy(text)
            auto_steps()

            translated_text = pyperclip.paste()
            if translated_text:
                for sub, trans_text in zip(group, translated_text.split(" @\n")):
                    sub.text = trans_text.replace(" ◍◍◍◍, ", ",\n")
                    sub.text = sub.text.replace(" ◍◍◍◍ ", "\n")
                    sub.text = sub.text.replace(" ◍◍◍◍", "")

        subs.save(os.path.join(dir_path, filename), encoding='utf-8')

        frezes = ["\nPrzetłumaczono z www.DeepL.com/Translator (wersja darmowa)\n",
                  "Przetłumaczono z www.DeepL.com/Translator (wersja darmowa)",
                  "\nTranslated with www.DeepL.com/Translator (free version)\n",
                  "\nTranslated with www.DeepL.com/Translator (free version)"]

        with open(os.path.join(dir_path, filename), 'r', encoding='utf-8') as in_file:
            text = in_file.read()

        for freze in frezes:
            text = text.replace(freze, "")

        with open(os.path.join(dir_path, filename), 'w', encoding='utf-8') as out_file:
            out_file.write(text)

    def translate_srt(self,  filename: str, dir_path: str, settings: Settings):
        translator = settings.translator
        translated_line_count = int(settings.translated_line_count)

        self.console.print(f"\nTłumaczenie napisów za pomocą {translator}...",
                           style='bold green')
        self.console.print(os.path.join(dir_path, filename))
        if translator == 'DeepL API':
            SubtitleTranslator.translate_deepl_api(
                filename, dir_path, translated_line_count, settings.deepl_api_key)
        elif translator == 'DeepL Desktop Free':
            SubtitleTranslator.translate_deepl_desktop(
                filename, dir_path, translated_line_count)
        elif translator == 'Google Translate':
            SubtitleTranslator.translate_google(
                filename, dir_path, translated_line_count)
        # Dodajemy tutaj inne tłumacze, gdy będą gotowe
