from Instruments.Config import client_oai
from Instruments.DB import get_history
from .Prompts import get_prompt
from .Converting import converting_city, converting_datetime, converting_conversation
from .TimeCorrection import get_current_dt


async def send_gpt(message, entity, user_id=None):
    if entity == 'datetime' or entity == 'conversation':
        now = await get_current_dt()
        if entity == 'conversation':
            history = await get_history(user_id)
            prompt = await get_prompt(message, entity, now, history)
        else:
            prompt = await get_prompt(message, entity, now)
    else:
        prompt = await get_prompt(message, entity)

    response = await client_oai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        n=1)

    formatted_msg = response.choices[0].message.content

    if entity == 'city':
        return await converting_city(formatted_msg)
    elif entity == 'datetime':
        return await converting_datetime(formatted_msg)
    elif entity == 'conversation':
        return await converting_conversation(formatted_msg)
