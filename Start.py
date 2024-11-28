from datetime import datetime
from fastapi import Request
from Instruments.Config import app
from Instruments.DB import add_new_user as anu, set_info, set_message, clear_history
from Formating.SendGPT import send_gpt
from Formating.TimeCorrection import correct_time
import uvicorn


@app.post("/")
async def handle_message(request: Request):
    data = await request.json()
    user_id = data['id']
    message = data.get('message')
    if message:
        await set_message(user_id, message)
        result = await send_gpt(message, 'conversation', user_id)
    else:
        result = await send_gpt('None', 'conversation', user_id)
    if isinstance(result, datetime):
        return {'text': 200, 'datetime': result}
    else:
        await set_message(user_id, result)
        return {'text': result}


@app.post("/id")
async def handle_id(request: Request):
    data = await request.json()
    user_id = data['id']
    await anu(user_id)


@app.post("/type")
async def handle_type(request: Request):
    data = await request.json()
    user_id = data['id']
    re_type = data['text']
    await set_info(user_id, re_type, 'type')


@app.post("/budget")
async def handle_budget(request: Request):
    data = await request.json()
    user_id = data['id']
    budget = data['text']
    await set_info(user_id, budget, 'budget')


@app.post("/city")
async def handle_city(request: Request):
    data = await request.json()
    user_id = data['id']
    probably_city = data['text']

    result = await send_gpt(probably_city,'city')
    if ' ' in result:
        return {'text': result}
    else:
        await set_info(user_id, result, 'city')
        return {'text': 200}


@app.post("/urgency")
async def handle_urgency(request: Request):
    data = await request.json()
    user_id = data['id']
    urgency = data['text']
    await set_info(user_id, urgency, 'urgency')


@app.post("/addons")
async def handle_addons(request: Request):
    data = await request.json()
    user_id = data['id']
    addons = data['text']
    await set_info(user_id, addons, 'addons')


@app.post("/datetime")
async def handle_datetime(request: Request):
    data = await request.json()
    user_id = data['id']
    probably_datetime = data['text']

    result = await send_gpt(probably_datetime, 'datetime')
    if isinstance(result, datetime):
        result = await correct_time(result)
        if isinstance(result, datetime):
            await set_info(user_id, result, 'datetime')
            str_datetime = result = result.replace(second=0)
            return {'text': 200, 'datetime': result, 'str_datetime': str_datetime}
    return {'text': result}


@app.post("/clear")
async def handle_clear(request: Request):
    data = await request.json()
    user_id = data['id']
    await clear_history(user_id)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
