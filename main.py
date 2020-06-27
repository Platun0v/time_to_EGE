from random import randint

import arrow
import requests
from loguru import logger

import config


class DateMessage:
    def __init__(self, text: str, date: arrow.Arrow):
        self.text = text
        self.date = date

    def get_message(self):
        delta = (self.date - arrow.now()).days
        if delta < 0:
            return ''
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
    DateMessage('До ЕГЭ по информатике осталось {}', arrow.Arrow(2020, 7, 3)),
    DateMessage('До ЕГЭ по русскому осталось {}', arrow.Arrow(2020, 7, 7)),
    DateMessage('До ЕГЭ по математике осталось {}', arrow.Arrow(2020, 7, 10)),
    DateMessage('До ЕГЭ по физике осталось {}', arrow.Arrow(2020, 7, 13)),
]


@logger.catch
def update():
    send_message('\n'.join(map(lambda x: x.get_message(), DATES)))


def send_message(text):
    requests.get(f'https://api.vk.com/method/messages.send', {
        'access_token': config.TOKEN,
        'v': '5.100',
        'peer_id': config.PEER_ID,
        'message': text,
        'random_id': randint(1, 10 ** 9)
    }).json()


if __name__ == '__main__':
    update()
