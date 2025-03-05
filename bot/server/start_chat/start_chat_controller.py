from telegram import Update
from telegram.ext import ContextTypes
import traceback

from .start_chat_service import StartChatService


class StartChatController:

    @staticmethod
    async def command_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        tg_id = update.message.from_user.id

        try:
            message = await StartChatService.get_meeting_message(tg_id)
        except Exception as e:
            message = e
            print(traceback.format_exc())

        await update.message.reply_text(message)
