import asyncio
from typing import Literal

from bot.services.gpt import ChatGPT
from bot.services.gpt_templates import SEASON_PLAN, GET_TALE_NAME_PROMPT, FIRST_CHAPTER_PROMPT, NEXT_CHAPTER_PROMPT


class TaleGetters:
    @staticmethod
    def get_season_plan(name: str, sex: Literal['Мальчик', 'Девочка'], age: int, interests: str):
        return SEASON_PLAN.format(sex=sex, name=name, age=age, interests=interests)

    @staticmethod
    def get_first_chapter(season_number: int):
        return FIRST_CHAPTER_PROMPT.format(season_number=season_number)

    @staticmethod
    def get_next_chapter():
        return NEXT_CHAPTER_PROMPT


class TaleGenerator:
    def __init__(self):
        self.gpt = ChatGPT()

    async def generate_tale_plan(self, name: str, sex: Literal['Мальчик', 'Девочка'], age: int,
                                 interests: str):
        return await self.gpt.get_text_by_prompt(TaleGetters.get_season_plan(name, sex, age, interests),
                                                 use_history=True)

    async def generate_tale_title(self):
        title = await self.gpt.get_text_by_prompt(GET_TALE_NAME_PROMPT)
        return title

    async def generate_first_chapter(self, season_num: int):
        first_chapter = await self.gpt.get_text_by_prompt(TaleGetters.get_first_chapter(season_num),
                                                          use_history=True)
        return first_chapter

    async def generate_next_chapter(self):
        new_chapter = await self.gpt.get_text_by_prompt(TaleGetters.get_next_chapter(),
                                                        use_history=True)
        return new_chapter
