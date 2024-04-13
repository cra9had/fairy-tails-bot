import asyncio
import json
import os
import openai
from openai import AsyncOpenAI
from typing import List, Optional, Dict, Literal
from .gpt_templates import SEASON_PLAN, FIRST_CHAPTER_PROMPT, NEXT_CHAPTER_PROMPT
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
            openai.session = session
        self.client = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.discussion: List[Optional[Dict]] = []
        self.model = "gpt-4-turbo"

    def dump(self):
        return json.dumps(
            {
                "messages": self.messages
            }
        )

    def loads(self, dump):
        self.messages = json.loads(dump)

    async def generate_first_series(self):
        return await self.get_text_by_prompt(FIRST_CHAPTER_PROMPT)

    async def generate_next_series(self):
        return await self.get_text_by_prompt(NEXT_CHAPTER_PROMPT)

    async def get_text_by_prompt(self, prompt: str, use_history: False) -> str:
        request = {
            "role": "user",
            "content": prompt
        }
        if use_history:
            chat_completion = await self.client.chat.completions.create(
                messages=[*self.discussion,
                          request],
                model=self.model,
            )

            self.discussion.extend(
                [request,
                 {
                     "role": "assistant",
                     "content": prompt
                 }]
            )

        else:
            chat_completion = await self.client.chat.completions.create(
                messages=[request],
                model=self.model,
            )

        return chat_completion.choices[0].message.content
