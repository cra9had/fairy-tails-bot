from aiogram.types import Message

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput


# handler for aiogram_dialog
async def child_name_handler(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data['name'] = message.text