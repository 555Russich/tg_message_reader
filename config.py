import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Self
from datetime import datetime

from dotenv import dotenv_values
from pydantic_settings import BaseSettings

DIR_PROJECT = Path(__file__).parent
DIR_SESSIONS = Path('sessions')
FILEPATH_ENV = Path('.env')
FILEPATH_SETTINGS = Path('settings.json')
FILEPATH_LOGGER = Path('tg_message_reader.log')

for d in [DIR_SESSIONS]:
    d.mkdir(exist_ok=True)


@dataclass
class Config:
    api_id: int | str
    api_hash: str


class Settings(BaseSettings):
    phone: str
    password: str
    chat_patterns: list[str]
    message_patterns: list[str]
    voice_speed_rate: int
    chat_ids: list[int] = field(default_factory=lambda: [])
    cbr_rate_datetimes: list[str | datetime] = field(default_factory=lambda: [])

    @property
    def session_filepath(self) -> str:
        return str((DIR_SESSIONS / self.phone).absolute())

    @classmethod
    def from_json(cls, filepath: Path) -> Self:
        return cls.model_validate_json(filepath.read_text(encoding='utf-8'))

    def convert_datetime(self):
        self.cbr_rate_datetimes = [datetime.strptime(s, '%d.%m.%Y %H:%M') for s in self.cbr_rate_datetimes]


env = dotenv_values(FILEPATH_ENV)
cfg = Config(**{k.lower(): v for k, v in env.items()})
settings = Settings.from_json(FILEPATH_SETTINGS)
settings.convert_datetime()
