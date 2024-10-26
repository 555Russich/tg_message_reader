import logging
import re
from datetime import datetime, timezone

from telethon import TelegramClient
from telethon.events import NewMessage
import pyttsx3


from config import FILEPATH_LOGGER
from config import cfg, settings
from my_logging import get_logger

client = TelegramClient(settings.session_filepath, cfg.api_id, cfg.api_hash,  system_version="4.16.30-vxCUSTOM_qwe")

engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    if voice.name == 'Microsoft Irina Desktop - Russian':
        engine.setProperty('voice', voice.id)
engine.setProperty('rate', settings.voice_speed_rate)
engine.runAndWait()


@client.on(NewMessage(chats=settings.chat_ids))
async def handle_message(event):
    delay = datetime.now(tz=timezone.utc) - event.date
    logging.info(f'Chat ID: {event.chat_id} | Delay: {delay.total_seconds()}')

    parts_to_pronounce = []
    for pattern in settings.message_patterns:
        for res in re.findall(pattern, event.message.raw_text):
            parts_to_pronounce.append(res)
    logging.info(f'Received event, parsed {len(parts_to_pronounce)} parts: {parts_to_pronounce}')

    text_to_pronounce = ' '.join(parts_to_pronounce)
    engine.say(text_to_pronounce)
    engine.runAndWait()


async def main():
    # This part is IMPORTANT, because it fills the entity cache.
    await client.get_dialogs()

    for chat_pattern in settings.chat_patterns:
        try:
            entity = await client.get_entity(chat_pattern)
            logging.info(f'Got entity: {entity.title} | {entity.id=}')
            settings.chat_ids.append(entity.id)
        except ValueError:
            logging.warning(f'!!! Could not find entity: {chat_pattern}')


if __name__ == '__main__':
    get_logger(FILEPATH_LOGGER)

    client.start(phone=settings.phone, password=settings.password)
    with client:
        try:
            client.loop.run_until_complete(main())
            client.run_until_disconnected()
        finally:
            logging.info(f'{client.is_connected()=}')
            client.session.save()
