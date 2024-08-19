from aiogram.types import Message

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from bot.states.user import MainWindow


# handler for aiogram_dialog
async def child_name_handler(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
    # HERE SOME LOGIC TO SET CHILD ACTUAL NAME TO DATABASE
    dialog_manager.dialog_data['name'] = message.text
    # maybe some logic to check if name is correct(idk maybe its not really necessary)
    await message.reply(f'Имя {message.text} успешно установлено')

    await dialog_manager.switch_to(MainWindow.all_child_settings)