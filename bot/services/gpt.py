import asyncio
import os
from openai import AsyncOpenAI
from typing import List, Optional, Dict, Literal
from .gpt_templates import SEASON_PLAN


class ChatGPT:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.messages: List[Optional[Dict]] = []
        self.model = "gpt-4-turbo"

    @staticmethod
    def get_season_plan(sex: Literal['Мальчик', 'Девочка'], name: str, age: int, interests: str):
        return SEASON_PLAN.format(sex=sex, name=name, age=age, interests=interests)

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
