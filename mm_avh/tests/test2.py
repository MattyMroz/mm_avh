import yaml

data = {
    "TRANSLATORS": [
        {
            "name": "Google Translate"
        },
        {
            "name": "DeepL API"
        },
        {
            "name": "DeepL Desktop Free"
        },
        {
            "name": "ChatGPT",
            "suboptions": [
                {
                    "name": "ChatGPT + Google Translate"
                },
                {
                    "name": "ChatGPT + DeepL API"
                },
                {
                    "name": "ChatGPT + DeepL Desktop"
                },
                {
                    "name": "ChatGPT + Google Translate + DeepL API"
                },
                {
                    "name": "ChatGPT + Google Translate + DeepL Desktop"
                }
            ]
        },
        {
            "name": "Edge AI",
            "suboptions": [
                {
                    "name": "Edge AI + Google Translate"
                },
                {
                    "name": "Edge AI + DeepL API"
                },
                {
                    "name": "Edge AI + DeepL Desktop"
                },
                {
                    "name": "Edge AI + Google Translate + DeepL API"
                },
                {
                    "name": "Edge AI + Google Translate + DeepL Desktop"
                }
            ]
        }
    ],
    "TRANSLATION OPTIONS": [
        {
            "name": "Ilość tłumaczonych linii na raz:",
            "suboptions": [
                {
                    "name": "30"
                },
                {
                    "name": "40"
                },
                {
                    "name": "50"
                },
                {
                    "name": "75"
                },
                {
                    "name": "100"
                }
            ]
        },
        {
            "name": "Czy tłumaczyć rozdzielone napisy?",
            "suboptions": [
                {
                    "name": True
                },
                {
                    "name": False
                }
            ]
        }
    ],
    "VOICE ACTORS": [
        {
            "name": "TTS - Zosia - Harpo",
            "description": {
                "speed": "Szybkość głosu od 0 do ... (słowa na minutę), domyślna: 200",
                "volume": "Głośność głosu od 0 do 1, domyślna: 0.7"
            },
            "default_options": {
                "default_voice_speed": 200,
                "default_voice_volume": 0.7
            }
        },
        {
            "name": "TTS - Agnieszka - Ivona",
            "description": {
                "speed": "Szybkość głosu od -10 do 10, domyślna: 5",
                "volume": "Głośność głosu od 0 do 100, domyślna: 65"
            },
            "default_options": {
                "default_voice_speed": 5,
                "default_voice_volume": 65
            }
        },
        {
            "name": "TTS - Zofia - Edge",
            "description": {
                "speed": "Szybkość głosu (+/- ? %) od -100% do +100%, domyślna: +40%",
                "volume": "Głośność głosu (+/- ? %) od -100% do +100%, domyślna: +0%"
            },
            "default_options": {
                "default_voice_speed": "+40%",
                "default_voice_volume": "+0%"
            }
        },
        {
            "name": "TTS - Marek - Edge",
            "description": {
                "speed": "Szybkość głosu (+/- ? %) od -100% do +100%, domyślna: +40%",
                "volume": "Głośność głosu (+/- ? %) od -100% do +100%, domyślna: +0%"
            },
            "default_options": {
                "default_voice_speed": "+40%",
                "default_voice_volume": "+0%"
            }
        }
    ],
    "OUTPUT": [
        {
            "name": "Oglądam w MM_AVH_Players (wynik: napisy i audio)"
        },
        {
            "name": "Scal do mkv"
        },
        {
            "name": "Wypal do mp4"
        }
    ]
}

with open('config.yaml', 'w') as file:
    yaml.safe_dump(data, file)
