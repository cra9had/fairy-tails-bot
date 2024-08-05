import asyncio
import json
from typing import Literal

from bot.services.gpt import ChatGPT
from bot.services.gpt_templates import SEASON_PLAN, GET_TALE_NAME_PROMPT, FIRST_CHAPTER_PROMPT, NEXT_CHAPTER_PROMPT, \
    SEASON_PLAN_PICTURE, SEASON_PLAN_CONTINUE


class TaleGetters:
    @staticmethod
    def get_season_plan(name: str, sex: Literal['Мальчик', 'Девочка'], age: int, interests: str):
        return SEASON_PLAN.format(sex=sex, name=name, age=age, interests=interests)

    @staticmethod
    def get_season_plan_continue():
        return SEASON_PLAN_CONTINUE

    @staticmethod
    def get_first_chapter(season_number: int):
        return FIRST_CHAPTER_PROMPT.format(season_number=season_number)

    @staticmethod
    def get_season_photo(tale_plan: str):
        return SEASON_PLAN_PICTURE.format(tale_plan=tale_plan)

    @staticmethod
    def get_next_chapter():
        return NEXT_CHAPTER_PROMPT


class TaleGenerator:
    def __init__(self, provided_history: list[str] | None = None):
        self.gpt = ChatGPT()

        if provided_history:
            self.gpt.discussion = provided_history

    async def generate_tale_plan(self, name: str, sex: Literal['Мальчик', 'Девочка'], age: int,
                                 interests: str):
        return (await self.gpt.get_text_by_prompt(TaleGetters.get_season_plan(name, sex, age, interests),
                                                  use_history=True)).replace('*', '').replace("#", "")

    async def generate_tale_plan_continue(self, provided_history: list | None = None):
        return (await self.gpt.get_text_by_prompt(TaleGetters.get_season_plan_continue(),
                                                  provided_history=provided_history)).replace('*', '').replace("#", "")

    async def generate_tale_title(self):
        title = await self.gpt.get_text_by_prompt(GET_TALE_NAME_PROMPT)
        return title

    async def generate_first_chapter(self, season_num: int, provided_history: list | None = None):
        first_chapter = await self.gpt.get_text_by_prompt(TaleGetters.get_first_chapter(season_num),
                                                          use_history=True, provided_history=provided_history)
        first_chapter = first_chapter.replace('*', '').replace("#", "")
        return first_chapter

    async def generate_next_chapter(self, provided_history: list | None = None):
        new_chapter = await self.gpt.get_text_by_prompt(TaleGetters.get_next_chapter(),
                                                        use_history=True, provided_history=provided_history)
        new_chapter = new_chapter.replace('*', '').replace('*', '').replace("#", "")

        return new_chapter

    async def generate_tale_season_photo(self, season_plan: str):
        photo_url = await self.gpt.get_photo_by_prompt(TaleGetters.get_season_photo(season_plan))
        return photo_url
