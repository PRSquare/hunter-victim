def getText(lang):
    if (lang == 'en'):
        return _text_en
    elif (lang == 'ru'):
        return _text_ru
    else:
        return _text_en # fallback

_text_en = {
    "stop-the-word": "Stop the word after all Foxes/Rabbits are dead",
    "word-size": "Word size",
    "rabbit-population": "Rabbit population",
    "foxes-population": "Foxes population",
    "food-amount": "Food amount",
    "food-growth-speed": "Food growth speed",
    "rabbit-stomach-capacity": "Rabbit tomach capacity",
    "fox-stomach-capacity": "Fox tomach capacity"
}

_text_ru = {
    "stop-the-word": "Остановить мир после смерти всех Лис/Зайцев",
    "word-size": "Размер Мира",
    "rabbit-population": "Популяция Зайцев",
    "foxes-population": "Популяция Лис",
    "food-amount": "Кол-во Еды",
    "food-growth-speed": "Темп Роста Еды",
    "rabbit-stomach-capacity": "Запас Еды Зайцев",
    "fox-stomach-capacity": "Запас Еды Лис"
}

