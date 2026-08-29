"""Keyword -> reply map for automatic responses.

Matching is case-insensitive and looks for the keyword anywhere in the
incoming message text. Edit this dict to customize the bot's replies.
"""

RESPONSES = {
    "привет": "Привет! Чем можем помочь?",
    "цена": "Актуальные цены смотрите в разделе «Товары» нашего сообщества.",
    "доставка": "Доставка осуществляется по всей России, сроки уточняйте у менеджера.",
    "контакт": "Связаться с менеджером можно по кнопке «Написать сообщение» в шапке сообщества.",
    "помощь": "Напишите свой вопрос, и мы ответим в ближайшее время. "
    "Также доступны ключевые слова: цена, доставка, контакт.",
}

DEFAULT_RESPONSE = (
    "Спасибо за сообщение! Мы скоро ответим. "
    "Попробуйте ключевые слова: цена, доставка, контакт, помощь."
)


def find_response(text: str) -> str:
    lowered = text.lower()
    for keyword, response in RESPONSES.items():
        if keyword in lowered:
            return response
    return DEFAULT_RESPONSE
