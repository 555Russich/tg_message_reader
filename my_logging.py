import logging
import sys
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo


TZ_MOSCOW = ZoneInfo('Europe/Moscow')


def get_logger(filepath: Path) -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        encoding='utf-8',
        format="[{asctime},{msecs:03.0f}]:[{levelname}]:{message}",
        datefmt='%d.%m.%Y %H:%M:%S',
        style='{',
        handlers=[
            logging.FileHandler(filepath, mode='a'),
            logging.StreamHandler(sys.stdout),
        ]
    )

    logging.Formatter.converter = lambda *args: datetime.now(tz=TZ_MOSCOW).timetuple()
    logging.getLogger('asyncio').setLevel(logging.WARNING)
    logging.getLogger('telethon').setLevel(logging.WARNING)
    logging.getLogger('comtypes').setLevel(logging.WARNING)
