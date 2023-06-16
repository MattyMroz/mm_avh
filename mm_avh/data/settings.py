import json
from dataclasses import dataclass
from typing import Optional
from rich.console import Console


console: Console = Console()


@dataclass
class Config:
    @staticmethod
    def get_translators():
        return [
            {'name': 'Google Translate'},
            {'name': 'DeepL API'},
            {'name': 'DeepL Desktop Free'},
            {
                'name': 'ChatGPT',
                'suboptions': [
                    {'name': 'ChatGPT + Google Translate'},
                    {'name': 'ChatGPT + DeepL API'},
                    {'name': 'ChatGPT + DeepL Desktop'},
                    {'name': 'ChatGPT + Google Translate + DeepL API'},
                    {'name': 'ChatGPT + Google Translate + DeepL Desktop'},
                ],
            },
            {
                'name': 'Edge AI',
                'suboptions': [
                    {'name': 'Edge AI + Google Translate'},
                    {'name': 'Edge AI + DeepL API'},
                    {'name': 'Edge AI + DeepL Desktop'},
                    {'name': 'Edge AI + Google Translate + DeepL API'},
                    {'name': 'Edge AI + Google Translate + DeepL Desktop'},
                ],
            },
        ]

    @staticmethod
    def get_translation_options():
        return [
            {'name': '30'},
            {'name': '40'},
            {'name': '50'},
            {'name': '75'},
            {'name': '100'},
        ]

    @staticmethod
    def get_voice_actors():
        return [
            {
                'name': 'TTS - Zosia - Harpo',
                'description': {
                    'speed': 'Szybkość głosu od 0 do ... (słowa na minutę), domyślna: 200',
                    'volume': 'Głośność głosu od 0 do 1, domyślna: 0.7',
                },
                'default_options': {
                    'default_voice_speed': 200,
                    'default_voice_volume': 0.7,
                },
            },
            {
                'name': 'TTS - Agnieszka - Ivona',
                'description': {
                    'speed': 'Szybkość głosu od -10 do 10, domyślna: 5',
                    'volume': 'Głośność głosu od 0 do 100, domyślna: 65',
                },
                'default_options': {
                    'default_voice_speed': 5,
                    'default_voice_volume': 65,
                },
            },
            {
                'name': 'TTS - Zofia - Edge',
                'description': {
                    'speed': 'Szybkość głosu (+/- ? %) od -100% do +100%, domyślna: +40%',
                    'volume': 'Głośność głosu (+/- ? %) od -100% do +100%, domyślna: +0%',
                },
                'default_options': {
                    'default_voice_speed': '+40%',
                    'default_voice_volume': '+0%',
                },
            },
            {
                'name': 'TTS - Marek - Edge',
                'description': {
                    'speed': 'Szybkość głosu (+/- ? %) od -100% do +100%, domyślna: +40%',
                    'volume': 'Głośność głosu (+/- ? %) od -100% do +100%, domyślna: +0%',
                },
                'default_options': {
                    'default_voice_speed': '+40%',
                    'default_voice_volume': '+0%',
                },
            },
        ]

    @staticmethod
    def get_output():
        return [
            {'name': 'Oglądam w MM_AVH_Players (wynik: napisy i audio)'},
            {'name': 'Scal do mkv'},
            {'name': 'Wypal do mp4'},
        ]


@dataclass
class Settings:
    translator: Optional[str] = None
    deepl_api_key: Optional[str] = None
    chat_gpt_access_token: Optional[str] = None
    edge_ai_cookies: Optional[str] = None
    translated_line_count: Optional[str] = None
    tts: Optional[str] = None
    tts_speed: Optional[str] = None
    tts_volume: Optional[str] = None
    output: Optional[str] = None

    @classmethod
    def load_from_file(cls, filename: str) -> Optional['Settings']:
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            console.print(f'[bold bright_red]Nie znaleziono pliku {filename}')
            return None
        except json.decoder.JSONDecodeError:
            console.print(f'[bold bright_red]Niepoprawny format pliku {filename}')
            return None

        return Settings(
            translator=data.get('translator'),
            deepl_api_key=data.get('deepl_api_key'),
            chat_gpt_access_token=data.get('chat_gpt_access_token'),
            edge_ai_cookies=data.get('edge_ai_cookies'),
            translated_line_count=data.get('translated_line_count'),
            tts=data.get('tts'),
            tts_speed=data.get('tts_speed'),
            tts_volume=data.get('tts_volume'),
            output=data.get('output')
        )

    @staticmethod
    def set_option(prompt: str, options: None) -> Optional[str]:
        console.print(f'\n[bold bright_yellow]{prompt}')
        for i, option in enumerate(options):
            console.print(f'[bold bright_yellow]{i + 1}.[/bold bright_yellow] [white]{option["name"]}')
            if 'suboptions' in option:
                for j, suboption in enumerate(option['suboptions']):
                    console.print(
                        f'[bold bright_yellow]    {i + 1}.{j + 1}.[/bold bright_yellow] [white]{suboption["name"]}')
            elif 'description' in option:
                console.print(f'    [white]{option["description"]["speed"]}')
                console.print(f'    [white]{option["description"]["volume"]}')
        console.print('[bold bright_green]Wybierz opcję: ', end='')
        choice = input()
        if '.' in choice:
            major_choice, minor_choice = map(int, choice.split('.'))
            if 1 <= major_choice <= len(options) and 1 <= minor_choice <= len(options[major_choice - 1]['suboptions']):
                return options[major_choice - 1]['suboptions'][minor_choice - 1]['name']
        elif choice.isdigit():
            choice_num = int(choice)
            if 1 <= choice_num <= len(options):
                return options[choice_num - 1]['name']
        else:
            for option in options:
                if option['name'] == choice:
                    return option['name']
        console.print('[bold bright_red]Niepoprawny wybór. Nie zmieniono wartości!')
        return None

    @staticmethod
    def is_valid_speed(speed: str, tts: str) -> bool:
        if tts == 'TTS - Zosia - Harpo':
            return int(speed) >= 0
        if tts == 'TTS - Agnieszka - Ivona':
            return -10 <= int(speed) <= 10
        if tts in {'TTS - Zofia - Edge', 'TTS - Marek - Edge'}:
            return speed.startswith(('+', '-')) and speed[1:-1].isdigit() and -100 <= int(
                speed[1:-1]) <= 100 and speed.endswith('%')
        return False

    @staticmethod
    def is_valid_volume(volume: str, tts: str) -> bool:
        if tts == 'TTS - Zosia - Harpo':
            return 0 <= float(volume) <= 1
        if tts == 'TTS - Agnieszka - Ivona':
            return -100 <= int(volume) <= 100
        if tts in {'TTS - Zofia - Edge', 'TTS - Marek - Edge'}:
            return volume.startswith(('+', '-')) and volume[1:-1].isdigit() and -100 <= int(
                volume[1:-1]) <= 100 and volume.endswith('%')
        return False

    @staticmethod
    def get_user_settings() -> Optional['Settings']:
        # Wczytanie ustawień z pliku settings.json, jeśli istnieje
        settings = Settings.load_from_file('settings.json')

        translator = Settings.set_option('Wybierz tłumacza: ', Config.get_translators())
        if translator is None:
            translator = settings.translator if settings else None

        console.print('\n[bold bright_yellow]Czy chcesz ustawić klucz API DeepL?')
        console.print('[bold bright_green]T lub Y - tak: ', end='')
        if input().lower() in ('t', 'y'):
            console.print(
                '[bold bright_yellow]Klucz API DeepL można wygenerować na stronie https://www.deepl.com/pro-api')
            console.print('[bold bright_green]Podaj klucz API DeepL: ', end='')
            deepl_api_key = input('')
            if deepl_api_key == '':
                deepl_api_key = settings.deepl_api_key if settings else None
                console.print('[bold bright_red]Niepoprawny wartość. Nie zmieniono wartości!')
        else:
            deepl_api_key = settings.deepl_api_key if settings else None

        console.print('\n[bold bright_yellow]Czy chcesz ustawić token dostępu do chat GPT?')
        console.print('[bold bright_green]T lub Y - tak: ', end='')
        if input().lower() in ('t', 'y'):
            console.print(
                '[bold bright_yellow]Token dostępu do chat GPT można wygenerować na stronie https://api.ai21.com/register')
            console.print('[bold bright_green]Podaj token dostępu do chat GPT: ', end='')
            chat_gpt_access_token = input()
            if chat_gpt_access_token == '':
                chat_gpt_access_token = settings.chat_gpt_access_token if settings else None
                console.print('[bold bright_red]Niepoprawny wartość. Nie zmieniono wartości!')
        else:
            chat_gpt_access_token = settings.chat_gpt_access_token if settings else None

        console.print('\n[bold bright_yellow]Czy chcesz ustawić ciasteczka Edge AI?')
        console.print('[bold bright_green]T lub Y - tak: ', end='')
        if input().lower() in ('t', 'y'):
            console.print('[bold bright_yellow]Ciasteczka Edge AI można wygenerować w przeglądarce Edge')
            console.print('[bold bright_green]Podaj ciasteczka Edge AI: ', end='')
            edge_ai_cookies = input()
            if edge_ai_cookies == '':
                edge_ai_cookies = settings.edge_ai_cookies if settings else None
                console.print('[bold bright_red]Niepoprawny wartość. Nie zmieniono wartości!')
        else:
            edge_ai_cookies = settings.edge_ai_cookies if settings else None

        translated_line_count = Settings.set_option(
            'Wybierz liczbę przetłumaczonych linii: ',
            Config.get_translation_options())
        if translated_line_count is None:
            translated_line_count = settings.translated_line_count if settings else None

        tts = Settings.set_option('Wybierz silnik TTS: ', Config.get_voice_actors())
        if tts is None:
            tts = settings.tts if settings else None

        default_speed = None
        default_volume = None
        voice_actor = next(
            (actor for actor in Config.get_voice_actors() if actor['name'] == tts),
            None)
        if voice_actor:
            default_speed = voice_actor['default_options']['default_voice_speed']
            default_volume = voice_actor['default_options']['default_voice_volume']

        console.print(f'\n[bold bright_yellow]Wybrałeś: {tts}')


        tts_speed = None
        console.print('[bold bright_green]Wpisz szybkość głosu: ', end='')
        tts_speed_choice = input()

        try:
            tts_speed = (
                tts_speed_choice if Settings.is_valid_speed(tts_speed_choice, tts)
                                    and tts_speed_choice.strip() != ''
                else default_speed
            )
        except ValueError:
            tts_speed = default_speed

        tts_volume = None
        console.print('[bold bright_green]Wpisz głośność głosu: ', end='')
        tts_volume_choice = input()

        try:
            tts_volume = (
                tts_volume_choice if Settings.is_valid_volume(tts_volume_choice, tts)
                                        and tts_volume_choice.strip() != ''
                else default_volume
            )
        except ValueError:
            tts_volume = default_volume

        output = Settings.set_option('Wybierz wyjście: ', Config.get_output())
        if output is None:
            output = settings.output if settings else None

        return Settings(
            translator=translator,
            deepl_api_key=deepl_api_key,
            chat_gpt_access_token=chat_gpt_access_token,
            edge_ai_cookies=edge_ai_cookies,
            translated_line_count=translated_line_count,
            tts=tts,
            tts_speed=tts_speed,
            tts_volume=tts_volume,
            output=output
        )


# Settings.get_user_settings()
console.print(Settings.get_user_settings())
x = input('Wciśnij Enter, aby kontynuować...')

# settings = Settings.load_from_file('settings.json')
# if settings:
#     print(settings.translator)
#     print(settings.deepl_api_key)
#     print(settings.chat_gpt_access_token)
#     print(settings.edge_ai_cookies)
#     print(settings.translated_line_count)
#     print(settings.tts)
#     print(settings.tts_speed)
#     print(settings.tts_volume)
#     print(settings.output)
# print(Config.get_translators())
# print(Config.get_translation_options())
# print(Config.get_voice_actors())
# print(Config.get_output())
