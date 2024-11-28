from Instruments.Config import DB


async def add_new_user(user_id):
    async with DB() as conn:
        await conn.execute('INSERT INTO users (id) VALUES ($1) ON CONFLICT (id) DO NOTHING', user_id)
        await conn.execute('INSERT INTO message_history (id) VALUES ($1) ON CONFLICT (id) DO NOTHING', user_id)


async def set_info(user_id, info, entity):
    async with DB() as conn:
        query = f'UPDATE users SET {entity} = $2 WHERE id = $1'
        await conn.execute(query, user_id, info)


async def set_message(user_id, message):
    async with DB() as conn:
        current_history = await conn.fetchval('SELECT history FROM message_history WHERE id = $1', user_id)
        if current_history is None:
            current_history = []
        current_history.append(message)

        if len(current_history) > 10:
            current_history.pop(0)
        await conn.execute('UPDATE message_history SET history = $2 WHERE id = $1', user_id, current_history)


async def get_history(user_id):
    async with DB() as conn:
        return await conn.fetchval('SELECT history FROM message_history WHERE id = $1', user_id)


async def clear_history(user_id):
    async with DB() as conn:
        await conn.execute('UPDATE message_history SET history = NULL WHERE id = $1', user_id)
