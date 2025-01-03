import logging
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import TZ_MOSCOW, settings
from src.speaker import speaker
from src.scrapper import (
    get_cb_key_rate,
)


scheduler = AsyncIOScheduler(
    job_defaults={'misfire_grace_time': 60},
    logger=logging.getLogger(),
    timezone=TZ_MOSCOW
)
CUR_CODES = ['USD', 'EUR', 'CNY']


async def get_cb_key_rate_and_represent(cbr_rate_dt: datetime):
    cbr_rate = await get_cb_key_rate(cbr_rate_dt)
    cbr_rate_str = f'{cbr_rate}%'
    print(f'СТАВКА ЦБ: {cbr_rate_str}')
    speaker.say(f'{cbr_rate}%')
    speaker.runAndWait()

    # try:
    #     cbr_rate_f = float(cbr_rate)
    #     if cbr_rate_f <= 21:
    #         print('LONG')
    #     elif cbr_rate_f == 22


def setup_scheduler():
    for cbr_rate_dt in settings.cbr_rate_datetimes:
        date_trigger = cbr_rate_dt - timedelta(seconds=30)
        scheduler.add_job(
            func=get_cb_key_rate_and_represent,
            kwargs={'cbr_rate_dt': cbr_rate_dt},
            trigger='date',
            run_date=date_trigger,
            name='CBR Key Rate scrapper',
            max_instances=1
        )
