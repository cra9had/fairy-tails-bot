import asyncio
import json
import os
from openai import AsyncOpenAI
from typing import List, Optional, Dict, Literal
from .gpt_templates import SEASON_PLAN, FIRST_SERIES, NEXT_SERIES
import requests
from requests.auth import HTTPProxyAuth



class ChatGPT:
    def __init__(self):
        if os.getenv("OPENAI_PROXY"):
            proxy = os.getenv("OPENAI_PROXY")
            proxy_auth = HTTPProxyAuth(os.getenv("OPENAI_PROXY_USERNAME"), os.getenv("OPENAI_PROXY_PASSWORD"))

            # Configure a session to use the proxy
            session = requests.Session()
            session.proxies = {'http': proxy, 'https': proxy}
            session.auth = proxy_auth
        self.client = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.messages: List[Optional[Dict]] = []
        self.model = "gpt-4-turbo"

    @staticmethod
    def get_season_plan(sex: Literal['Мальчик', 'Девочка'], name: str, age: int, interests: str):
        return SEASON_PLAN.format(sex=sex, name=name, age=age, interests=interests)

    def dump(self):
        return json.dumps(
            {
                "messages": self.messages
            }
        )

    @classmethod
    def loads(cls, dump):
        obj = cls()
        obj.messages = json.loads(dump)
        return obj

    async def generate_first_series(self):
        return await self.get_text_by_prompt(FIRST_SERIES)

    async def generate_next_series(self):
        return await self.get_text_by_prompt(NEXT_SERIES)

    async def get_text_by_prompt(self, prompt: str) -> str:
        request = {
            "role": "user",
            "content": prompt
        }
        chat_completion = await self.client.chat.completions.create(
            messages=[*self.messages,
                      request],
            model=self.model,
        )
        self.messages.extend(
            [request,
             {
                 "role": "assistant",
                 "content": prompt
             }]
        )
        return chat_completion.choices[0].message.content
