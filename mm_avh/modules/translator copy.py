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
from revChatGPT.V1 import Chatbot
import re

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
        command = os.path.join(
            os.environ['APPDATA'], 'Programs', 'Zero Install', '0install-win.exe')
        args = ["run", "--no-wait",
                "https://appdownload.deepl.com/windows/0install/deepl.xml"]
        subprocess.call([command] + args)

        time.sleep(7)

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
        pyautogui.hotkey('alt', 'f4')

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

    @staticmethod
    def translate_chat_gpt(filename, dir_path, translated_line_count, chat_gpt_access_token):
        chatbot = Chatbot(config={"access_token": chat_gpt_access_token})

        subs = pysrt.open(os.path.join(dir_path, filename), encoding='utf-8')
        groups = [subs[i:i+translated_line_count]
                for i in range(0, len(subs), translated_line_count)]

        additional_info = ""
        while True:
            info = input(
                "Dodaj dodatkowe informacje o tłumaczonym tekście (opcjonalnie): ")
            if info == "":
                break
            additional_info += info + ", "

        counter = 1
        for group in groups:
            text = ""
            for sub in group:
                text += "◍◍{}. {}".format(counter, sub.text.replace('\n', ' ◍◍◍◍ ')) + " @@\n"
                counter += 1
            text = text.rstrip(' @@\n')

            prompt = """NAJWAŻNIEJSZE: JEŚLI DOSTANIESZ NAPISY NP. 1 DO 30 TO ZWRÓĆ NAPISY 1 DO 30 NAWET JEŚLI TŁUMACZENIE DANEGO NAPISU JEST GŁUPIE, NIESPÓJNE, I OGÓLNIE ZŁĘ, BŁĄDNY NAPIS JEST LEPSZY NIŻ JEGO BRAK
Jesteś moim tłumaczem, specjalizującym się w przekładzie na język polski. Twoja rola nie ogranicza się do prostego tłumaczenia - jesteś również redaktorem i ulepszaczem języka. Komunikuję się z Tobą w różnych językach, a Twoim zadaniem jest identyfikowanie języka, tłumaczenie go i odpowiadanie poprawioną i ulepszoną wersją mojego tekstu, w języku polskim.

Zanim przystąpisz do tłumaczenia, poświęć chwilę na zrozumienie gramatycznych, językowych i kontekstualnych niuansów tekstu. Uchwyc subtelności i upewnij się, że tekst płynie jak strumień słów, jakby ktoś nam opowiadał historię, czytał audiobooka, czy narrację filmu, bo ostatecznie ten tekst będzie czytany na głos.

Twoim zadaniem jest podniesienie poziomu mojego języka, zastępując uproszczone słowa i zdania na poziomie C0 bardziej wyszukanymi i eleganckimi wyrażeniami. Zachowaj oryginalne znaczenie, ale uczyn język bardziej literackim. Twoje odpowiedzi powinny ograniczać się do poprawionego i ulepszonego tłumaczenia, bez dodatkowych wyjaśnień.

Podczas tłumaczenia, zachowaj dyskrecję w decydowaniu, kiedy tłumaczyć słowa dosłownie, a kiedy zachować zapożyczenia w ich oryginalnej formie. Unikaj używania polskich odpowiedników, które zniekształcają znaczenie lub estetykę zdania.

Zachowaj oryginalne formatowanie tekstu - nie dodawaj żadnych dodatkowych spacji, tabulatorów ani znaków nowej linii. Tekst, który tłumaczysz, może również przedstawiać akcje z książki, więc miej to na uwadze.

Podejdź globalnie do tekstu. Jeśli gdziekolwiek w tekście podano informacje o płci postaci, użyj tych informacji, aby kierować swoim tłumaczeniem przez cały tekst. Na przykład, zamiast tłumaczyć "I did it" jako "Zrobiłem to" lub "Zrobiłam to", przetłumacz to jako "To zostało zrobione przeze mnie", jeśli płeć nie jest określona. To podejście zmniejsza błędy tłumaczenia. Globalne podejście, nie tłumacz iteracyjnie słowo po słowie,  na przykład : "Święty Tyrs przegrał. Ona umarła.",  gdzie poprawnie to: "Święta Tyrs przegrała. Ona umarła."

Bądź kreatywny w swoich tłumaczeniach, dostosowując swój ton do kontekstu - bądź dowcipny dla lekkich tekstów i dodaj powagi i profesjonalizmu dla poważnych. Tłumacz wszystkie przekleństwa, nie cenzuruj i nie zmieniaj znaczenia słów, które są ważne w kontekście lub które zmieniają emocjonalny ton tekstu.

W tekście symbol '◍◍◍◍' reprezentuje nową linię w tym samym napisie, a symbol '@@' reprezentuje koniec napisu. Jeśli postanowisz pominąć jakiś napis, z jakichś powodów pamiętaj o zostawieniu znaku '@@', jest to kluczowe dla dalszego działania programu tłumaczeniowego. Nie zmieniaj ilości znaków '@@'.

Twoim ostatecznym celem jest wyprodukowanie tłumaczenia, które jest jak najbardziej wiernie odwzorowane na oryginał, zarówno pod względem znaczenia, jak i poprawności gramatycznej i syntaktycznej, chyba że oryginał jest niegramatyczny.

Zadanie wykonuj powoli krok po kroku

Dodatkowe informacje na temat tekstu który ma być tłumaczony: """ + additional_info + "\n\nTeraz przetłumacz poniższe napisy:\n" + text

            prev_text = ""
            for data in chatbot.ask(
                prompt,
            ):
                prev_text = data["message"]

            translated_text = prev_text
            if translated_text:
                translated_lines = translated_text.split(" @@\n")
                if len(translated_lines) != len(group):
                    print(f"Błąd: liczba napisów po tłumaczeniu ({len(translated_lines)}) nie jest taka sama jak przed tłumaczeniem ({len(group)})")
                for sub, trans_text in zip(group, translated_lines):
                    trans_text = re.sub(r"◍◍\d+\. ", "", trans_text)
                    trans_text = trans_text.replace(" ◍◍◍◍, ", ",\n")
                    trans_text = trans_text.replace(" ◍◍◍◍ ", "\n")
                    trans_text = trans_text.replace(" ◍◍◍◍", "")
                    sub.text = trans_text

        subs.save(os.path.join(dir_path, filename), encoding='utf-8')






    def translate_srt(self,  filename: str, dir_path: str, settings: Settings):
        translator = settings.translator
        translated_line_count = int(settings.translated_line_count)

        self.console.print(f"Tłumaczenie napisów za pomocą {translator}...",
                           style='bold green')
        self.console.print(os.path.join(dir_path, filename))

        translator_functions = {
            'Google Translate': lambda *args:
                SubtitleTranslator.translate_google(*args[:3]),
            'DeepL API':
                SubtitleTranslator.translate_deepl_api,
            'DeepL Desktop Free': lambda *args:
                SubtitleTranslator.translate_deepl_desktop(*args[:3]),
            'ChatGPT': lambda *args:
                SubtitleTranslator.translate_chat_gpt(
                    *args[:3], settings.chat_gpt_access_token)
        }

        if translator in translator_functions:
            translator_functions[translator](
                filename, dir_path, translated_line_count)
        else:
            self.console.print(
                f"Nieznany translator: {translator}", style='bold red')
