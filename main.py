
import os
import asyncio
import re
from telethon import TelegramClient, events

API_ID = int(os.environ["37560710"])
API_HASH = os.environ["73b521601e4442ff21957069f16c589f"]

CHANNEL = os.environ["@nftrix1"]
OLD = os.environ["@awersone"]
NEW = os.environ["@oppcount"]

client = TelegramClient("session", API_ID, API_HASH)

def replace_username(text):
    if not text:
        return text

    return re.sub(
        re.escape(OLD) + r"(?![a-zA-Z0-9_])",
        NEW,
        text,
        flags=re.IGNORECASE
    )

async def main():
    await client.start()

    entity = await client.get_entity(CHANNEL)

    print("Проверяю старые публикации...")

    async for message in client.iter_messages(entity):
        if message.text and OLD.lower() in message.text.lower():
            updated = replace_username(message.text)
            await message.edit(updated)
            print("Изменён пост:", message.id)
            await asyncio.sleep(1)

    print("Старые посты обработаны. Слежу за новыми.")

    @client.on(events.NewMessage(chats=entity))
    async def handler(event):
        text = event.message.text
        if text and OLD.lower() in text.lower():
            await event.message.edit(replace_username(text))

    await client.run_until_disconnected()

asyncio.run(main())
