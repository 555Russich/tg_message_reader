import asyncio
import logging
from datetime import datetime

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from config import TZ_MOSCOW


async def scrap_cb_rate(session: ClientSession) -> float:
    async with session.get(url='https://www.cbr.ru/') as r:
        html = await r.text()
        soup = BeautifulSoup(html, 'lxml')
        div_content = soup.find('a', href='/hd_base/KeyRate/').parent.parent
        divs_rate = div_content.find_all('div', class_='main-indicator_line')

        for div_rate in divs_rate:
            a_date = div_rate.find('a')
            date_str = a_date.text.strip().replace('с ', '')
            rate_date = datetime.strptime(date_str, '%d.%m.%Y').replace(tzinfo=TZ_MOSCOW)
            rate_str = div_rate.find('div', class_='main-indicator_value').text.strip()
            rate_value = float(rate_str.replace('%', '').replace(',', '.'))

            if rate_date > datetime.now(tz=TZ_MOSCOW):
                return rate_value


async def get_cb_rate(cbr_rate_dt: datetime):
    async with ClientSession() as session:
        while True:
            seconds_left = (cbr_rate_dt - datetime.now(tz=TZ_MOSCOW)).total_seconds()
            if seconds_left > 10:
                sleep_time = 2
            elif seconds_left > 2:
                sleep_time = 0.5
            else:
                sleep_time = 0

            new_cb_rate = await scrap_cb_rate(session)
            logging.info(f'СТАВКА ЦБ: {new_cb_rate}')

            if isinstance(new_cb_rate, float):
                return new_cb_rate

            await asyncio.sleep(sleep_time)
