"""
    Module settings provides a Config and Settings classes.
    Config class contains static methods to get the configuration options.
    Settings class contains methods to change the settings. (Static methods *_*)

    * Example usage:
    Settings.change_settings_save_to_file('settings.json')
    - If the file does not exist, it will be created with default settings.
    - If the file exists, it will be overwritten with the current settings.
    - If the file exists, but the settings are incomplete,
        the missing settings will be added with default values.

    * Example default settings in settings.json:
        {
        "translator": "Google Translator",
        "deepl_api_key": "null",
        "chat_gpt_access_token": null,
        "edge_ai_cookies": null,
        "translated_line_count": "50",
        "tts": "TTS - Agnieszka - Ivona",
        "tts_speed": "5",
        "tts_volume": "65",
        "output": "Ogl\u0105dam w MM_AVH_Players (wynik: napisy i audio)"
        }
"""

import json
from dataclasses import dataclass, asdict
from typing import Optional, Tuple, List, Dict
from rich.console import Console

console: Console = Console()


@dataclass(slots=True)
class Config:
    """
    Config class contains static methods to get the configuration options.
    """

    @staticmethod
    def get_translators() -> List[Dict[str, str]]:
        """
        Returns a list of available translators.

        Each translator is represented as a dictionary with the following keys:
        - 'name': The name of the translator.
        - 'suboptions' (optional): A list of suboptions for the translator.

        Returns:
            List[Dict[str, str]]: A list of translators.
        """
        return [
            {'name': 'Google Translate'},
            {'name': 'DeepL API'},
            {'name': 'DeepL Desktop Free'},
            {
                'name': 'ChatGPT',
                'suboptions': [
                    {'name': 'ChatGPT + Google Translate'}
                ],
            },
            {
                'name': 'Edge AI',
                'suboptions': [
                    {'name': 'Edge AI + Google Translate'}
                ],
            },
        ]

    @staticmethod
    def get_translation_options() -> List[Dict[str, str]]:
        """
        Returns a list of available translation options.

        Each option is represented as a dictionary with the following key:
        - 'name': The name of the option.

        Returns:
            List[Dict[str, str]]: A list of translation options.
        """
        return [
            {'name': '30'},
            {'name': '40'},
            {'name': '50'},
            {'name': '75'},
            {'name': '100'},
        ]

    @staticmethod
    def get_voice_actors() -> List[Dict[str, str]]:
        """
        Returns a list of available voice actors for text-to-speech.

        Each voice actor is represented as a dictionary with the following keys:
        - 'name': The name of the voice actor.
        - 'description': A dictionary containing the description of the voice actor, including:
            - 'speed': The speed of the voice actor.
            - 'volume': The volume of the voice actor.
        - 'default_options': A dictionary containing the default options for the voice actor, including:
            - 'default_voice_speed': The default speed of the voice actor.
            - 'default_voice_volume': The default volume of the voice actor.

        Returns:
            List[Dict[str, str]]: A list of voice actors.
        """
        return [
            {
                'name': 'TTS - Zosia - Harpo',
                'description': {
                    'speed': 'Szybkość głosu od 0 do ... (słowa na minutę), domyślna: 200',
                    'volume': 'Głośność głosu od 0 do 1, domyślna: 0.7',
                },
                'default_options': {
                    'default_voice_speed': '200',
                    'default_voice_volume': '0.7',
                },
            },
            {
                'name': 'TTS - Agnieszka - Ivona',
                'description': {
                    'speed': 'Szybkość głosu od -10 do 10, domyślna: 5',
                    'volume': 'Głośność głosu od 0 do 100, domyślna: 65',
                },
                'default_options': {
                    'default_voice_speed': '5',
                    'default_voice_volume': '65',
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
            {
                'name': 'TTS - *Głos* - ElevenLans',
                'description': {
                    'speed': 'Szybkość głosu: Auto',
                    'volume': 'Głośność głou: Auto',
                },
                'default_options': {
                    'default_voice_speed': 'auto',
                    'default_voice_volume': 'auto',
                },
            },
        ]

    @staticmethod
    def get_output() -> List[Dict[str, str]]:
        """
        Returns a list of available output options.

        Each option is represented as a dictionary with the following key:
        - 'name': The name of the output option.

        Returns:
            List[Dict[str, str]]: A list of output options.
        """
        return [
            {'name': 'Oglądam w MM_AVH_Players (wynik: napisy i audio)'},
            {'name': 'Scal do mkv'},
            {'name': 'Wypal do mp4'},
        ]


@dataclass(slots=True)
class Settings:
    """
    A class representing application settings.

    Attributes:
        translator (Optional[str]): The selected translator.
        deepl_api_key (Optional[str]): The API key for DeepL translation service.
        chat_gpt_access_token (Optional[str]): The access token for ChatGPT API.
        edge_ai_cookies (Optional[str]): The Edge AI cookies.
        translated_line_count (Optional[str]): The number of translated lines.
        tts (Optional[str]): The selected TTS engine.
        tts_speed (Optional[str]): The speed of the TTS voice.
        tts_volume (Optional[str]): The volume of the TTS voice.
        output (Optional[str]): The selected output option.

    Methods:
        load_from_file(cls, filename: str) -> 'Settings': Load settings from a file.
        set_option(prompt: str, options: List[Dict[str, str]]) -> str | None: Set an option from a list of options.
        is_valid_speed(speed: str, tts: str) -> bool: Check if a given speed value is valid for the selected TTS engine.
        is_valid_volume(volume: str, tts: str) -> bool: Check if a given volume value is valid for the selected TTS engine.
        get_translator(settings: Optional['Settings']) -> Optional[str]: Get the selected translator.
        get_deepl_api_key(settings: Optional['Settings']) -> Optional[str]: Get the DeepL API key.
        get_chat_gpt_access_token(settings: Optional['Settings']) -> Optional[str]: Get the ChatGPT access token.
        get_edge_ai_cookies(settings: Optional['Settings']) -> Optional[str]: Get the Edge AI cookies.
        get_translated_line_count(settings: Optional['Settings']) -> Optional[str]: Get the number of translated lines.
        get_tts(settings: Optional['Settings']) -> Optional[str]: Get the selected TTS engine.
        get_default_speed_volume(tts: str) -> Tuple[Optional[str], Optional[str]]: Get the default speed and volume for a TTS engine.
        get_tts_speed(tts: str, default_speed: Optional[str]) -> Optional[str]: Get the TTS speed.
        get_tts_volume(tts: str, default_volume: Optional[str]) -> Optional[str]: Get the TTS volume.
        get_output(settings: Optional['Settings']) -> Optional[str]: Get the selected output option.
        get_user_settings(filename: str) -> Optional['Settings']: Get user settings from a file.
        change_settings_save_to_file(filename: str) -> None: Change and save settings to a file.
    """
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
    def load_from_file(cls, filename: str) -> 'Settings':
        """
        Load settings from a JSON file.

        Args:
            filename (str): The name of the file to load settings from.

        Returns:
            Settings: An instance of the Settings class with the loaded settings.

        Raises:
            FileNotFoundError: If the file does not exist.
            json.decoder.JSONDecodeError: If the file has an invalid JSON format.
        """

        def get_default_settings():
            return cls(
                translator='Google Translator',
                deepl_api_key=None,
                chat_gpt_access_token=None,
                edge_ai_cookies=None,
                translated_line_count='50',
                tts='TTS - Agnieszka - Ivona',
                tts_speed='5',
                tts_volume='65',
                output='Oglądam w MM_AVH_Players (wynik: napisy i audio)'
            )

        try:
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            console.print(f'[bold bright_red]Nie znaleziono pliku {filename}')
            return get_default_settings()

        except json.decoder.JSONDecodeError:
            console.print(
                f'[bold bright_red]Niepoprawny format pliku {filename}')
            return get_default_settings()

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
    def set_option(prompt: str, options: List[Dict[str, str]]) -> str | None:
        """
        Set an option from a list of options.

        Args:
            prompt (str): The prompt to display to the user.
            options (List[Dict[str, str]]): The list of options to choose from.

        Returns:
            str | None: The selected option, or None if the selection is invalid.

        Raises:
            No specific exceptions are raised.
        """
        console.print(f'\n[bold bright_yellow]{prompt}')
        for i, option in enumerate(options):
            console.print(
                f'[bold bright_yellow]{i + 1}.[/bold bright_yellow] [white]{option["name"]}')
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
        console.print(
            '[bold bright_red]Niepoprawny wybór. Nie zmieniono wartości!')
        return None

    @staticmethod
    def is_valid_speed(speed: str, tts: str) -> bool:
        """
        Check if a given speed value is valid for the selected TTS engine.

        Args:
            speed (str): The speed value to check.
            tts (str): The selected TTS engine.

        Returns:
            bool: True if the speed value is valid, False otherwise.

        Raises:
            No specific exceptions are raised.
        """
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
        """
        Check if a given volume value is valid for the selected TTS engine.

        Args:
            volume (str): The volume value to check.
            tts (str): The selected TTS engine.

        Returns:
            bool: True if the volume value is valid, False otherwise.

        Raises:
            No specific exceptions are raised.
        """
        if tts == 'TTS - Zosia - Harpo':
            return 0 <= float(volume) <= 1
        if tts == 'TTS - Agnieszka - Ivona':
            return -100 <= int(volume) <= 100
        if tts in {'TTS - Zofia - Edge', 'TTS - Marek - Edge'}:
            return volume.startswith(('+', '-')) and volume[1:-1].isdigit() and -100 <= int(
                volume[1:-1]) <= 100 and volume.endswith('%')
        return False

    @staticmethod
    def get_translator(settings: Optional['Settings']) -> Optional[str]:
        """
        Retrieve the selected translator from the user settings or prompt the user to choose one.

        Args:
            settings (Optional['Settings']): The user settings object.

        Returns:
            Optional[str]: The selected translator or None if not found.

        Raises:
            No specific exceptions are raised.
        """

        translator = Settings.set_option(
            'Wybierz tłumacza: ', Config.get_translators())
        if translator is None:
            translator = settings.translator if settings else None
        return translator

    @staticmethod
    def get_deepl_api_key(settings: Optional['Settings']) -> Optional[str]:
        """
        Prompt the user to set the DeepL API key or retrieve it from the user settings.

        Args:
            settings (Optional['Settings']): The user settings object.

        Returns:
            Optional[str]: The DeepL API key or None if not set.

        Raises:
            No specific exceptions are raised.
        """

        console.print(
            '\n[bold bright_yellow]Czy chcesz ustawić klucz API DeepL?')
        console.print('[bold bright_green]T lub Y - tak: ', end='')
        if input().lower() in ('t', 'y'):
            console.print(
                '[bold bright_yellow]Klucz API DeepL można wygenerować na stronie https://www.deepl.com/pro-api')
            console.print('[bold bright_green]Podaj klucz API DeepL: ', end='')
            deepl_api_key = input('')
            if deepl_api_key == '':
                deepl_api_key = settings.deepl_api_key if settings else None
                console.print(
                    '[bold bright_red]Niepoprawna wartość. Nie zmieniono wartości!')
        else:
            deepl_api_key = settings.deepl_api_key if settings else None
        return deepl_api_key

    @staticmethod
    def get_chat_gpt_access_token(settings: Optional['Settings']) -> Optional[str]:
        """
        Prompt the user to set the Chat GPT access token or retrieve it from the user settings.

        Args:
            settings (Optional['Settings']): The user settings object.

        Returns:
            Optional[str]: The Chat GPT access token or None if not set.

        Raises:
            No specific exceptions are raised.
        """

        console.print(
            '\n[bold bright_yellow]Czy chcesz ustawić token dostępu do chat GPT?')
        console.print('[bold bright_green]T lub Y - tak: ', end='')
        if input().lower() in ('t', 'y'):
            console.print(
                '[bold bright_yellow]Token dostępu (accessToken): https://chat.openai.com/api/auth/session')
            console.print(
                '[bold bright_green]Podaj token dostępu do chat GPT: ', end='')
            chat_gpt_access_token = input()
            if chat_gpt_access_token == '':
                chat_gpt_access_token = settings.chat_gpt_access_token if settings else None
                console.print(
                    '[bold bright_red]Niepoprawna wartość. Nie zmieniono wartości!')
        else:
            chat_gpt_access_token = settings.chat_gpt_access_token if settings else None
        return chat_gpt_access_token

    @staticmethod
    def get_edge_ai_cookies(settings: Optional['Settings']) -> Optional[str]:
        """
        Prompt the user to set the Edge AI cookies or retrieve them from the user settings.

        Args:
            settings (Optional['Settings']): The user settings object.

        Returns:
            Optional[str]: The Edge AI cookies or None if not set.

        Raises:
            No specific exceptions are raised.
        """

        console.print(
            '\n[bold bright_yellow]Czy chcesz ustawić ciasteczka Edge AI?')
        console.print('[bold bright_green]T lub Y - tak: ', end='')
        if input().lower() in ('t', 'y'):
            console.print(
                '[bold bright_yellow]Ciasteczka Edge AI można wygenerować w przeglądarce Edge')
            console.print(
                '[bold bright_green]Podaj ciasteczka Edge AI: ', end='')
            edge_ai_cookies = input()
            if edge_ai_cookies == '':
                edge_ai_cookies = settings.edge_ai_cookies if settings else None
                console.print(
                    '[bold bright_red]Niepoprawna wartość. Nie zmieniono wartości!')
        else:
            edge_ai_cookies = settings.edge_ai_cookies if settings else None
        return edge_ai_cookies

    @staticmethod
    def get_translated_line_count(settings: Optional['Settings']) -> Optional[str]:
        """
        Prompt the user to set the number of translated lines or retrieve it from the user settings.

        Args:
            settings (Optional['Settings']): The user settings object.

        Returns:
            Optional[str]: The number of translated lines or None if not set.

        Raises:
            No specific exceptions are raised.
        """

        translated_line_count = Settings.set_option('Wybierz liczbę przetłumaczonych linii: ',
                                                    Config.get_translation_options())
        if translated_line_count is None:
            translated_line_count = settings.translated_line_count if settings else None
        return translated_line_count

    @staticmethod
    def get_tts(settings: Optional['Settings']) -> Optional[str]:
        """
        Prompt the user to choose a TTS engine or retrieve it from the user settings.

        Args:
            settings (Optional['Settings']): The user settings object.

        Returns:
            Optional[str]: The selected TTS engine or None if not set.

        Raises:
            No specific exceptions are raised.
        """

        tts = Settings.set_option(
            'Wybierz silnik TTS: ', Config.get_voice_actors())
        if tts is None:
            tts = settings.tts if settings else None
        return tts

    @staticmethod
    def get_default_speed_volume(tts: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Retrieve the default voice speed and volume for the specified TTS engine.

        Args:
            tts (str): The selected TTS engine.

        Returns:
            Tuple[Optional[str], Optional[str]]: A tuple containing the default voice speed and volume,
                or (None, None) if not found.

        Raises:
            No specific exceptions are raised.
        """

        default_speed = None
        default_volume = None
        voice_actor = next(
            (actor for actor in Config.get_voice_actors() if actor['name'] == tts), None)
        if voice_actor:
            default_speed = voice_actor['default_options']['default_voice_speed']
            default_volume = voice_actor['default_options']['default_voice_volume']
        return default_speed, default_volume

    @staticmethod
    def get_tts_speed(tts: str, default_speed: Optional[str]) -> Optional[str]:
        """
        Prompt the user to enter the voice speed for the selected TTS engine, or use the default speed.

        Args:
            tts (str): The selected TTS engine.
            default_speed (Optional[str]): The default voice speed for the TTS engine.

        Returns:
            Optional[str]: The selected voice speed or the default speed if not set.

        Raises:
            No specific exceptions are raised.
        """

        console.print('[bold bright_green]Wpisz szybkość głosu: ', end='')
        tts_speed_choice = input()
        try:
            tts_speed = tts_speed_choice if (
                Settings.is_valid_speed(
                    tts_speed_choice, tts) and tts_speed_choice.strip() != ''
            ) else default_speed
        except ValueError:
            tts_speed = default_speed
        return tts_speed

    @staticmethod
    def get_tts_volume(tts: str, default_volume: Optional[str]) -> Optional[str]:
        """
        Prompt the user to enter the voice volume for the selected TTS engine, or use the default volume.

        Args:
            tts (str): The selected TTS engine.
            default_volume (Optional[str]): The default voice volume for the TTS engine.

        Returns:
            Optional[str]: The selected voice volume or the default volume if not set.

        Raises:
            No specific exceptions are raised.
        """

        console.print('[bold bright_green]Wpisz głośność głosu: ', end='')
        tts_volume_choice = input()
        try:
            tts_volume = tts_volume_choice if (
                Settings.is_valid_volume(
                    tts_volume_choice, tts) and tts_volume_choice.strip() != ''
            ) else default_volume
        except ValueError:
            tts_volume = default_volume
        return tts_volume

    @staticmethod
    def get_output(settings: Optional['Settings']) -> Optional[str]:
        """
        Prompt the user to choose an output option or retrieve it from the user settings.

        Args:
            settings (Optional['Settings']): The user settings object.

        Returns:
            Optional[str]: The selected output option or None if not set.

        Raises:
            No specific exceptions are raised.
        """

        output = Settings.set_option('Wybierz wyjście: ', Config.get_output())
        if output is None:
            output = settings.output if settings else None
        return output

    @staticmethod
    def get_user_settings(filename: str) -> Optional['Settings']:
        """
        Get the user settings from a file or prompt the user to enter them.

        Args:
            filename (str): The name of the settings file.

        Returns:
            Optional['Settings']: The user settings object or None if not found.

        Raises:
            No specific exceptions are raised.
        """

        settings = Settings.load_from_file(filename)

        translator = Settings.get_translator(settings)
        deepl_api_key = Settings.get_deepl_api_key(settings)
        chat_gpt_access_token = Settings.get_chat_gpt_access_token(settings)
        edge_ai_cookies = Settings.get_edge_ai_cookies(settings)
        translated_line_count = Settings.get_translated_line_count(settings)
        tts = Settings.get_tts(settings)
        default_speed, default_volume = Settings.get_default_speed_volume(tts)
        console.print(f'\n[bold bright_yellow]Wybrałeś: {tts}')
        tts_speed = Settings.get_tts_speed(tts, default_speed)
        tts_volume = Settings.get_tts_volume(tts, default_volume)
        output = Settings.get_output(settings)

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

    @staticmethod
    def change_settings_save_to_file(filename: str) -> None:
        """
        Prompt the user to change the settings and save them to a file.

        Args:
            filename (str): The name of the settings file.

        Returns:
            None

        Raises:
            No specific exceptions are raised.
        """

        settings = Settings.get_user_settings(filename)

        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(asdict(settings), file, indent=4)
