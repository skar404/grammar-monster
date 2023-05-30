from typing import Set

from pydantic import BaseSettings


class Settings(BaseSettings):
    openai_token: str

    token: str
    api_id: str
    api_hash: str

    is_memory: bool = True

    available_chats: Set[int] = set()

    tmp_chat: int

    class Config:
        env_file = '.env', '../.env'


settings = Settings()
