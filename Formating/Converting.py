import re
from datetime import datetime
import pytz


async def converting_datetime(msg):
    if msg.lower().strip('"') == 'время':
        return 'Вы не ввели время'
    elif msg.lower().strip('"') == 'дата':
        return 'Вы не ввели дату'
    elif msg.lower().strip('"') == 'дата и время':
        return 'Вы не ввели дату и время'
    else:
        try:
            return datetime.strptime(msg, "%Y-%m-%d %H:%M")
        except ValueError:
            return 'Не удалось распознать дату и время'


async def converting_city(msg):
    if msg.lower().strip('"') == 'несколько городов':
        return 'Введите только 1 город'
    elif msg.lower().strip('"') == 'город из списка':
        return 'К сожалению этот город не поддерживается'
    elif msg.lower().strip('"') == 'город не из россии':
        return 'Мы работаем только по России'
    elif msg.lower().strip('"') == 'город не из россии':
        return 'Мы работаем только по России'
    elif msg.lower().strip('"') == 'нет города':
        return 'Вы не ввели город'
    elif msg.lower().strip('"') == 'вопрос':
        return 'Доступны все города России, за исключением городов: Томск, Воронеж, Рязань, Саранск.'
    elif ' ' in msg:
        return 'Не удалось распознать город'
    else:
        return msg


async def converting_conversation(msg):
    pattern = r'\d{4}-\d{2}-\d{2} (?:в )?\d{2}:\d{2}'
    match = re.search(pattern, msg)

    if match:
        try:
            datetime_obj = datetime.strptime(match.group(0).replace(' в ', ' '), "%Y-%m-%d %H:%M")
            moscow_tz = pytz.timezone('Europe/Moscow')
            meet_dt = moscow_tz.localize(datetime_obj)
            return meet_dt
        except ValueError:
            return msg
    else:
        return msg

