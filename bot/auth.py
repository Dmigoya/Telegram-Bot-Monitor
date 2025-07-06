from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from bot.security import is_authorized


def auth_required(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if await is_authorized(update):
            return await func(update, context, *args, **kwargs)
        await update.message.reply_text("\ud83d\udeab No autorizado.")
    return wrapper

