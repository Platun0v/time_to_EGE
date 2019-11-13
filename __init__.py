from random import randint

from .timer import Timer
import datetime
import arrow
import requests


PEER_ID = 475552069
TOKEN = 'ec932e44e27f149ee204d48143fa244883cfb72e5bcda7ee2c1f762167487f171ae87e8d2d6eeebbdfe7c'


class DateMessage:
    def __init__(self, text: str, date: arrow.Arrow):
        self.text = text
        self.date = date

    def get_message(self):
        delta = (self.date - arrow.now()).days
        return self.text.format(f'{delta} {self.normal_days_name(delta)}')

    @staticmethod
    def normal_days_name(days):
        days = str(days)
        if len(days) > 1 and days[-2] == '1':
            return 'дней'
        elif days[-1] in ['0', '5', '6', '7', '8', '9']:
            return 'дней'
        elif days[-1] == '1':
            return 'день'
        elif days[-1] in ['2', '3', '4']:
            return 'дня'


DATES = [
    DateMessage('До итогового сочинения осталось {}', arrow.Arrow(2019, 12, 4)),
    DateMessage('До ЕГЭ осталось {}', arrow.Arrow(2020, 5, 25)),
]

WHEN_TO_CALL = datetime.time(9, 37, 0)


def start():
    t = Timer(update)
    t.call_everyday((WHEN_TO_CALL,))
    t.run()


def update():
    send_message('\n'.join(map(lambda x: x.get_message(), DATES)))


def send_message(text):
    requests.get(f'https://api.vk.com/method/messages.send', {
        'access_token': TOKEN,
        'v': '5.100',
        'peer_id': PEER_ID,
        'message': text,
        'random_id': randint(1, 10**9)
    }).json()


start()
