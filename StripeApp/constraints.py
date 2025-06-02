MAX_NAME_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 10_000
DEFAULT_CURRENCY = 'USD'
API_KEY = 'sk_test_51RUcJKQWV56vHYpOAH9T9jF4ZLNRYd6TsZ7YhzitzOzo7iJn4sMmu2xGo9e3IbRZf7y5w6z90Su4w6BS7Cb7X2t600d1xlOEXK'
MAX_DESCRIPTION_PREVIEW_SIZE = 100
SHORT_ENDING = '...'
NUMBERS_AFTER_DOT = 2
NUMBER_STEPS = 3
MIN_DISCOUNT = 5
MAX_DISCOUNT = 100
PERCENTS = 100
CURRENCY_CODE_CHARS = 3
CURRENCY_CODE_CHOICES = {
    'RUB': 'rk_test_51RUcJKQWV56vHYpOomPp7pWwuON34CY7Cw1Yd2Wjk4AMfMif6qlzppJmuj2zPSODr7iifDk0KTQ0BhsHprwElwpt00y92r2a7X',
    'USD': 'rk_test_51RUcJKQWV56vHYpO0fXKG0xl6AyYS1EZezIw5JfHaN3CCDEuHXtfDPsWXZOHUDjTyCZuB1ChlxktU9b73OTZIrdA00WZgA1pdg'
}
API_KEY_LENGTH = len(API_KEY)


def setup_dots(number: int) -> str:
    str_number = str(number)

    return_str = str_number[:len(str_number) % NUMBER_STEPS]

    for number_index in range(len(str_number) % NUMBER_STEPS, len(str_number), NUMBER_STEPS):
        return_str = f'{return_str}.{str_number[number_index:number_index + NUMBER_STEPS]}'

    return return_str


def cut_text(text: str):
    if not len(text):
        return None

    if len(text) < MAX_DESCRIPTION_PREVIEW_SIZE:
        return text

    return f'{text[:MAX_DESCRIPTION_PREVIEW_SIZE + len(SHORT_ENDING)]}' \
           f'{SHORT_ENDING}'
