from random import randint

from .timer import Timer
import datetime
import arrow
import requests


PEER_ID = 475552069
TOKEN = '9fa4fa588c99f77063d80794265609a80b19f9f58330324f93ce3d5d6d6e624668fa508373a9446ab5a34'


FINAL_ESSAY = 'До итогового сочинения осталось {}'
FINAL_ESSAY_DATE = arrow.Arrow(2019, 12, 4)

EGE = 'До ЕГЭ осталось {}'
EGE_DATE = arrow.Arrow(2020, 5, 25)

WHEN_TO_CALL = datetime.time(0, 0, 0)


def main():
    timer = Timer(update)
    timer.call_everyday((WHEN_TO_CALL,))
    timer.start()


def update():
    delta_essay = abs((arrow.now() - FINAL_ESSAY_DATE).days)
    delta_ege = abs((arrow.now() - EGE_DATE).days)
    text1 = FINAL_ESSAY.format(f'{delta_essay} {normal_days_name(delta_essay)}')
    text2 = EGE.format(f'{delta_ege} {normal_days_name(delta_ege)}')

    send_message(f'{text1}\n{text2}')


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


def send_message(text):
    requests.get(f'https://api.vk.com/method/messages.send', {
        'access_token': TOKEN,
        'v': '5.100',
        'peer_id': PEER_ID,
        'message': text,
        'random_id': randint(1, 10**9)
    })


if __name__ == '__main__':
    main()
