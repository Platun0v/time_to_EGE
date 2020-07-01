from typing import Tuple
from random import randint

import arrow
import requests
from loguru import logger

import config


class DateMessage:
    def __init__(self, text: str, date: arrow.Arrow):
        self.text = text
        self.date = date

    def get_message(self) -> str:
        delta = (self.date - arrow.now()).days
        if delta < 0:
            return ''

        norm_names = self.normal_days_name(delta)
        return self.text.format(date=f'{norm_names[0]} {delta} {norm_names[1]}')

    @staticmethod
    def normal_days_name(days: int) -> Tuple[str, str]:
        days = str(days)
        if len(days) > 1 and days[-2] == '1':
            return 'осталось', 'дней'
        elif days[-1] in ['0', '5', '6', '7', '8', '9']:
            return 'осталось', 'дней'
        elif days[-1] == '1':
            return 'остался', 'день'
        elif days[-1] in ['2', '3', '4']:
            return 'осталось', 'дня'


class EGEDateMessage(DateMessage):
    def __init__(self, subject: str, date: arrow.Arrow,
                 base: str = 'До ЕГЭ по {subject} {date}',
                 on_day: str = 'Всем удачи на ЕГЭ по {subject}!'):
        super().__init__(base.format(subject=subject, date='{date}'), date)

        if (self.date - arrow.now()).days == 0:
            self.text = on_day.format(subject=subject)


DATES = [
    EGEDateMessage('информатике', arrow.Arrow(2020, 7, 3, hour=10, tzinfo='UTC+3')),
    EGEDateMessage('русскому', arrow.Arrow(2020, 7, 7, hour=10, tzinfo='UTC+3')),
    EGEDateMessage('математике', arrow.Arrow(2020, 7, 10, hour=10, tzinfo='UTC+3')),
    EGEDateMessage('физике', arrow.Arrow(2020, 7, 13, hour=10, tzinfo='UTC+3')),
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
