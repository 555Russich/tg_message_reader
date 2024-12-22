import asyncio
import logging
import re
from datetime import datetime, timedelta, date, timezone

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from pandas import DataFrame
from tvDatafeed import TvDatafeed, Interval

from config import TZ_MOSCOW


async def get_cb_key_rate(dt_cbr_rate: datetime):
    async with ClientSession() as session:
        while True:
            seconds_left = (dt_cbr_rate - datetime.now(tz=TZ_MOSCOW)).total_seconds()
            if seconds_left > 10:
                sleep_time = 2
            elif seconds_left > 2:
                sleep_time = 0.5
            else:
                sleep_time = 0

            new_cb_rate = await scrap_cb_key_rate(session, dt_cbr_rate=dt_cbr_rate)

            if isinstance(new_cb_rate, float):
                logging.info(f'СТАВКА ЦБ: {new_cb_rate}')
                return new_cb_rate

            await asyncio.sleep(sleep_time)


async def scrap_cb_key_rate(session: ClientSession, dt_cbr_rate: datetime) -> float:
    async with session.get(url='https://www.cbr.ru/press/keypr') as r:
        html = await r.text()
        soup = BeautifulSoup(html, 'lxml')

    dt_modified_str = soup.find('head').find('meta', attrs={'name': 'zoom:last-modified'}).get('content')
    dt_modified_utc = datetime.strptime(dt_modified_str, '%a, %d %b %Y %H:%M:%S %Z').replace(tzinfo=timezone.utc)
    dt_modified_msc = dt_modified_utc.astimezone(tz=TZ_MOSCOW)

    if dt_modified_msc == dt_cbr_rate:
        title = soup.find('head').find('title').text
        key_rate = float(re.search(r'(\d+,\d+)(?=%)', title).group(0).replace(',', '.'))
        return key_rate
    return False
