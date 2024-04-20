from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_tail_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='ПОЛУЧИТЬ СКАЗКУ', callback_data='get_tail')]
            # handling in bot/handlers/get_tail_callback_handler
        ]
    )

    return keyboard


def get_episode_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Следующая серия', callback_data='get_next_episode')]
            # handling in bot/handlers/get_next_episode_callback_handler
        ]
    )

    return keyboard


def get_loop1_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Начать', callback_data='start_button')]
        ]
    )

    return keyboard


def get_loop2_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Подписка есть', callback_data='get_next_episode')]
        ]
    )

    return keyboard


def get_loop4_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Купить по Акции', callback_data='discount_button')]
        ]
    )

    return keyboard
