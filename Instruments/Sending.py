import aiohttp
from Instruments.Config import url, access_token


async def send_message(user_id, text):
    params = {"access_token": access_token}

    data = {
        "recipient": {"id": user_id},
        "message": {"text": text}}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, params=params, json=data) as response:
            if response.status == 200:
                print("Message sent successfully")
                response_data = await response.json()
                print(response_data)
            else:
                print(f"Failed to send message: {response.status}")
                response_data = await response.json()
                print(response_data)


async def main():
    user_id = "1120468703419248"
    message_text = "Привет, как я могу помочь?"
    await send_message(user_id, message_text)
