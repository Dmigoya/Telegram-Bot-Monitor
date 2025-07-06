import asyncio
import os
from importlib import import_module
from pathlib import Path
from telegram import BotCommand
from telegram.ext import Application, CommandHandler, ContextTypes

START_MSG = "\u2705 Bot de notificaciones conectado"
STOP_MSG = "\u274C Bot de notificaciones detenido"

from bot import notifier
from bot.auth import auth_required

CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 300))

_dynamic_handlers = []


async def send_startup() -> None:
    for uid in notifier.REPORT_IDS:
        await notifier.bot.send_message(chat_id=uid, text=START_MSG)


async def send_shutdown() -> None:
    for uid in notifier.REPORT_IDS:
        await notifier.bot.send_message(chat_id=uid, text=STOP_MSG)


def discover_modules():
    modules = []
    for file in Path(__file__).parent.joinpath("modules").glob("*.py"):
        if file.stem == "__init__":
            continue
        mod = import_module(f"bot.modules.{file.stem}")
        modules.append(mod)
    return modules


def build_handler(mod):
    async def handler(update, context):
        await mod.run(update, context)
    return handler


async def register_dynamic_commands(app: Application):
    for h in _dynamic_handlers:
        app.remove_handler(h, group=1)
    _dynamic_handlers.clear()
    commands = []
    for mod in discover_modules():
        handler = CommandHandler(mod.CMD_NAME, auth_required(build_handler(mod)))
        app.add_handler(handler, group=1)
        _dynamic_handlers.append(handler)
        commands.append(BotCommand(mod.CMD_NAME, mod.CMD_DESC))
    await app.bot.set_my_commands(commands)


async def refresh(update, context):
    await register_dynamic_commands(context.application)
    await update.message.reply_text("\ud83d\udd04 Comandos recargados")


async def report_job(context: ContextTypes.DEFAULT_TYPE):
    await notifier.send_report()

async def periodic_reports():
    while True:
        await notifier.send_report()
        await asyncio.sleep(CHECK_INTERVAL)


async def post_init(application: Application) -> None:
    await register_dynamic_commands(application)
    await send_startup()
    if application.job_queue:
        application.job_queue.run_repeating(report_job, interval=CHECK_INTERVAL)
    else:
        application.create_task(periodic_reports())


async def post_shutdown(application: Application) -> None:
    await send_shutdown()


def main() -> None:
    """Start the bot with dynamic command support."""
    app = (
        Application.builder()
        .token(os.getenv("BOT_TOKEN"))
        .post_init(post_init)
        .post_shutdown(post_shutdown)
        .build()
    )
    app.add_handler(CommandHandler("refresh", auth_required(refresh)), group=0)
    app.run_polling()


if __name__ == "__main__":
    main()

