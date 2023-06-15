# def set_settings(dir_path, settings):
#     translator_options = {
#         '1': 'Google Translate',
#         '2': 'DeepL API',
#         '3': 'DeepL Desktop',
#         '4': 'ChatGPT 3.5 Free'
#     }

#     translated_line_count_options = {
#         '1': '30',
#         '2': '50',
#         '3': '75',
#         '4': '100',
#     }

#     alt_main_translator_options = {
#         '1': 'yes',
#         '2': 'no'
#     }

#     tts_voice_options = {
#         '1': {
#             'name': 'TTS - Zosia - Harpo',
#             'speed_default': '200',
#             'volume_default': '0.7'
#         },
#         '2': {
#             'name': 'TTS - Agnieszka - Ivona',
#             'speed_default': '5',
#             'volume_default': '65'
#         },
#         '3': {
#             'name': 'TTS - Zofia - Edge',
#             'speed_default': '+40%',
#             'volume_default': '+0%'
#         },
#         '4': {
#             'name': 'TTS - Marek - Edge',
#             'speed_default': '+40%',
#             'volume_default': '+0%'
#         }
#     }

#     output_options = {
#         '1': 'Oglądam w MM_AVH_Players',
#         '2': 'Scal do mkv',
#         '3': 'Wypal do mp4',
#     }

#     cprint("╔═════════════════ Ustawienia ═════════════════╗\n",
#            'white', attrs=['bold'])
#     translator_choice = set_option(
#         "Wybierz translatora:", translator_options
#     )

#     deepl_api_key = ''
#     cprint("\nCzy chcesz ustawić klucz API DeepL? (t / y = tak):",
#            'yellow', attrs=['bold'], end=" ")
#     change_settings = input("")
#     if change_settings.lower() in ['t', 'y', 'tak', 'yes']:
#         cprint('Wpisz klucz API DeepL:', 'green', attrs=['bold'], end=' ')
#         deepl_api_key = input()
#         if deepl_api_key == '':
#             cprint("Pominięto.", 'red', attrs=['bold'])
#             if settings['deepl_api_key']:
#                 deepl_api_key = settings['deepl_api_key']
#     else:
#         cprint("Pominięto.", 'red', attrs=['bold'])
#         if settings['deepl_api_key']:
#             deepl_api_key = settings['deepl_api_key']

#     access_token = ''
#     cprint("\nCzy chcesz ustawić token dostępu do ChatGPT? (t / y = tak):",
#            'yellow', attrs=['bold'], end=" ")
#     change_settings = input()
#     if change_settings.lower() in ['t', 'y', 'tak', 'yes']:
#         url = "https://chat.openai.com/api/auth/session"
#         webbrowser.open(url)
#         cprint('Wpisz token dostępu do ChatGPT:',
#                'green', attrs=['bold'], end=' ')
#         access_token = input()
#         if access_token == '':
#             cprint("Pominięto.", 'red', attrs=['bold'])
#             if settings['access_token']:
#                 access_token = settings['access_token']
#     else:
#         cprint("Pominięto.", 'red', attrs=['bold'])
#         if settings['access_token']:
#             access_token = settings['access_token']

#     translated_line_count_choice = set_option(
#         "\nWybierz ilość tłumaczonych linii na raz:", translated_line_count_options
#     )
#     alt_main_translator_choice = set_option(
#         "\nCzy tłumaczyć rozdzielone napisy?", alt_main_translator_options
#     )
#     tts_choice = None
#     while tts_choice is None:
#         tts_choice = set_option(
#             "\nWybierz głos lektora:", tts_voice_options
#         )
#         if tts_choice not in tts_voice_options:
#             tts_choice = '2'  # Ustawienie domyślnej wartości

#     tts_speed_default = tts_voice_options.get(tts_choice).get('speed_default')

#     cprint("\nObesługiwane zakresy szybkości:",
#            'yellow', attrs=['bold'])
#     print("TTS - Zosia - Harpo     - szybkość głosu od 0 do ... (słowa na minute), domyślna: 200)")
#     print("TTS - Agnieszka - Ivona - szybkość głosu od -10 do 10 (domyślna: 5)")
#     print("TTS - Zofia - Edge      - szybkość głosu (+/-) od -100% do +100%, (domyślna: +40%)")
#     print("TTS - Marek - Edge      - szybkość głosu (+/-) od -100% do +100%, (domyślna: +40%)")

#     cprint(f"\nWpisz szybkość głosu (domyślna: {tts_speed_default}):", 'green', attrs=[
#            'bold'], end=" ")
#     tts_speed_choice = input('')
#     try:
#         tts_speed = (
#             tts_speed_choice if is_valid_speed(tts_speed_choice, tts_choice) and tts_speed_choice.strip() != ''
#             else tts_speed_default
#         )
#     except Exception:
#         tts_speed = tts_speed_default
#     cprint("\nObesługiwane zakresy głośności:", 'yellow', attrs=['bold'])
#     print("TTS - Zosia - Harpo     - głośność głosu od 0 do 1 (domyślna: 0.7)")
#     print("TTS - Agnieszka - Ivona - głośność głosu od 0 do 100 (domyślna: 65)")
#     print("TTS - Zofia - Edge      - głośność głosu (+/-) od -100% do +100%, (domyślna: +0%)")
#     print("TTS - Marek - Edge      - głośność głosu (+/-) od -100% do +100%, (domyślna: +0%)")
#     tts_volume_default = tts_voice_options.get(
#         tts_choice).get('volume_default')
#     cprint(f"\nWpisz głośność głosu (domyślna: {tts_volume_default}):", 'green', attrs=[
#            'bold'], end=" ")
#     tts_volume_choice = input('')
#     try:
#         tts_volume = (
#             tts_volume_choice if is_valid_volume(tts_volume_choice, tts_choice) and tts_volume_choice.strip() != ''
#             else tts_volume_default
#         )
#     except Exception:
#         tts_volume = tts_volume_default

#     output_options_choice = set_option(
#         "\nWybierz sposób wyjścia:", output_options
#     )

#     settings_data = {
#         'translator': translator_options.get(translator_choice, 'Google Translate'),
#         # jeśli nie jest pusty 1df708bf-af10-3e70-e577-b2d4cb763d74:fx
#         'deepl_api_key': deepl_api_key,
#         'access_token': access_token,
#         'translated_line_count': translated_line_count_options.get(translated_line_count_choice, '50'),
#         'alt_main_translator': alt_main_translator_options.get(alt_main_translator_choice, 'no'),
#         'tts': tts_voice_options.get(tts_choice).get('name', 'TTS - Agnieszka - Ivona'),
#         'tts_speed': tts_speed,
#         'tts_volume': tts_volume,
#         'output': output_options.get(output_options_choice, 'Oglądam w MM_AVH_Players')
#     }

#     with open(os.path.join(dir_path, 'src', 'settings.json'), 'w') as settings_file:
#         json.dump(settings_data, settings_file, indent=4)

#     cprint("Ustawienia zostały zapisane.\n", 'green', attrs=['bold'])


# USTAWIENIA

# TRANSLATORY
# 1.        Google Translate
# 2.        DeepL API
# 3.        DeepL Desktop
# 4.        ChatGPT
#   1.      ChatGPT + Google Translate
#   2.      ChatGPT + DeepL API
#   3.      ChatGPT + DeepL Desktop
#   4.      ChatGPT + Google Translate + DeepL API
#   5.      ChatGPT + Google Translate + DeepL Desktop
# 6.        Edge AI
#   1.      Edge AI + Google Translate
#   2.      Edge AI + DeepL API
#   3.      Edge AI + DeepL Desktop
#   4.      Edge AI + Google Translate + DeepL API
#   5.      Edge AI + Google Translate + DeepL Desktop

# OPCJE TŁUMACZENIA
# 1.        Ilość tłumaczonych linii na raz
#   1.      30
#   2.      40
#   3.      50
#   4.      75
#   5.      100
# 2.        Czy tłumaczyć rozdzielone napisy?
#   1.      Tak
#   2.      Nie

# GŁOSY LEKTORA
# 1.        TTS - Zosia - Harpo
# OPIS:
#   speed      TTS - Zosia - Harpo - szybkość głosu od 0 do ... (słowa na minute), domyślna: 200)
#   volume      TTS - Zosia - Harpo - głośność głosu od 0 do 1 (domyślna: 0.7)
# Opcjie domyślne:
#   default_voice_speed = 200
#   default_voice_volume = 0.7


# 2.      TTS - Agnieszka - Ivona
# OPIS:
#   Szybkość      TTS - Agnieszka - Ivona - szybkość głosu od -10 do 10 (domyślna: 5)
#   Głośność      TTS - Agnieszka - Ivona - głośność głosu od 0 do 100 (domyślna: 65)
# Opcjie domyślne:
#   default_voice_speed = 5
#   default_voice_volume = 65

# 3.      TTS - Zofia - Edge
# OPIS:
#   Szybkość      TTS - Zofia - Edge - szybkość głosu (+/-) od -100% do +100%, (domyślna: +40%)
#   Głośność      TTS - Zofia - Edge - głośność głosu (+/-) od -100% do +100%, (domyślna: +0%)
# Opcjie domyślne:
#   default_voice_speed = +40%
#   default_voice_volume = +0%


# 4.      TTS - Marek - Edge
# OPIS:
#   Szybkość      TTS - Marek - Edge - szybkość głosu (+/-) od -100% do +100%, (domyślna: +40%)
#   Głośność      TTS - Marek - Edge - głośność głosu (+/-) od -100% do +100%, (domyślna: +0%)
# Opcjie domyślne:
#   default_voice_speed = +40%
#   default_voice_volume = +0%


# WYJŚCIE
# 1.        Oglądam w MM_AVH_Players (napisy + audio)
# 2.        Scal do mkv
# 3.        Wypal do mp4

class Pies:
    def __init__(self, imie: str, wiek: str):
        self.imie = imie
        self.wiek = wiek

    def szczekaj(self):
        print("Hau Hau!")

    def podaj_wiek(self):
        print(f"Wiek: {self.wiek}")

    def podaj_imie(self):
        print(f"Imie: {self.imie}")


pies1 = Pies("Burek", 3)
pies2 = Pies("Azor", 5)

pies: Pies = Pies("Burek", "5")
pies.szczekaj()
pies.podaj_imie()
pies.podaj_wiek()

pies1.szczekaj()  # Wywołanie metody szczekaj na obiekcie pies1
print(pies2.imie)  # Wypis
