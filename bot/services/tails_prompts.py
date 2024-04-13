import asyncio
from typing import Literal

from bot.services.gpt import ChatGPT
from bot.services.gpt_templates import SEASON_PLAN, GET_TALE_NAME_PROMPT


class TaleGetters:
    @staticmethod
    def get_season_plan(name: str, sex: Literal['Мальчик', 'Девочка'], age: int, interests: str):
        return SEASON_PLAN.format(sex=sex, name=name, age=age, interests=interests)


class TaleGenerator:
    def __init__(self):
        self.gpt = ChatGPT()

    async def generate_tale_plan(self, name: str, sex: Literal['Мальчик', 'Девочка'], age: int,
                                 interests: str):
        return await self.gpt.get_text_by_prompt(TaleGetters.get_season_plan(name, sex, age, interests),
                                                 use_history=True)

    async def generate_tale_title(self):
        title = await self.gpt.get_text_by_prompt(GET_TALE_NAME_PROMPT, use_history=True)
        return title
