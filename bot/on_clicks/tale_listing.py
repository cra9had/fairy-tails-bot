from pprint import pprint

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Button

from bot.db.orm import create_tale
from bot.services.tales_prompts import TaleGenerator
from bot.states.user import Tail


async def get_chapter(event_from_user, dialog_manager: DialogManager, **kwargs):

    tale_plan = dialog_manager.dialog_data.get('tale_plan')
    tale_title = dialog_manager.dialog_data.get('tale_title')
    session = dialog_manager.dialog_data.get('session')

    tale_generator: TaleGenerator = dialog_manager.dialog_data.get('tale_generator')
    season = dialog_manager.dialog_data.get('season', 1)
    curr_chapter = dialog_manager.dialog_data.get('curr_chapter', 1)
    curr_episode = dialog_manager.dialog_data.get('curr_episode', 1)

    pprint(tale_generator.gpt.discussion)

    if curr_chapter == 1 and curr_episode == 1:
        await create_tale(session, tale_title, tale_plan, event_from_user.id)
        chapt_text = await tale_generator.generate_first_chapter(season_num=season)

    else:
        chapt_text = await tale_generator.generate_next_chapter()

    dialog_manager.dialog_data.update({'curr_chapter': curr_chapter + 1})
    if curr_chapter == 5:
        dialog_manager.dialog_data.update({'curr_episode': curr_episode + 1})
        dialog_manager.dialog_data.update({'curr_chapter': 1})

    dialog_manager.dialog_data.update({'tale_generator': tale_generator})

    return {'tale_title': tale_title,
            'season': season,
            'episode': curr_episode,
            'chapter': curr_chapter,
            'chapter_text': chapt_text}
