import logging
import re

from telethon import TelegramClient
from telethon.events import NewMessage
import pyttsx3


from config import FILEPATH_LOGGER
from config import cfg
from my_logging import get_logger

client = TelegramClient(cfg.session_filepath, cfg.api_id, cfg.api_hash,  system_version="4.16.30-vxCUSTOM_qwe")

engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    if voice.name == 'Microsoft Irina Desktop - Russian':
        engine.setProperty('voice', voice.id)
engine.setProperty('rate', 300)
engine.runAndWait()


@client.on(NewMessage(chats=cfg.chat_patterns))
async def handle_message(event):
    parts_to_pronounce = []
    for pattern in cfg.message_patterns:
        for res in re.findall(pattern, event.message.text):
            parts_to_pronounce.append(res)

    logging.info(f'Received event, parsed {len(parts_to_pronounce)} parts: {parts_to_pronounce}\n'
                 f'Original message: {event.message.text}')
    for text in parts_to_pronounce:
        engine.say(text)
        engine.runAndWait()


async def main():
    # This part is IMPORTANT, because it fills the entity cache.
    for d in await client.get_dialogs():
        print(d)
        print(d.id)

    entity = await client.get_entity('ORACLE NEWS | MOEX')
    print(entity)


if __name__ == '__main__':
    get_logger(FILEPATH_LOGGER)

    client.start(phone=cfg.phone, password=cfg.password)
    with client:
        try:
            client.loop.run_until_complete(main())
            client.run_until_disconnected()
        finally:
            logging.info(f'{client.is_connected()=}')
            client.session.save()
