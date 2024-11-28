from datetime import datetime, timedelta
import pytz


async def correct_time(meet_dt):
    moscow_tz = pytz.timezone('Europe/Moscow')
    meet_dt = moscow_tz.localize(meet_dt)
    now = datetime.now(moscow_tz)
    month_later = now + timedelta(days=30)

    if meet_dt < now:
        return "Вы указали время в прошлом"

    if meet_dt > month_later:
        return "Время слишком далеко в будущем. Укажите дату в пределах месяца."

    if not (10 <= meet_dt.hour < 19):
        return "Время должно быть между 10:00 и 19:00."

    if (meet_dt - now) < timedelta(minutes=62):
        return "Время должно быть как минимум на 62 минуты позже текущего."

    return meet_dt


async def get_current_dt():
    moscow_tz = pytz.timezone('Europe/Moscow')
    now = datetime.now(moscow_tz).strftime('%Y-%m-%d %H:%M')
    return now
