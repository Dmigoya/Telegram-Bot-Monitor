"""Gestión de permisos y baneo en memoria"""
import os
import time
from telegram import Update
from telegram.ext import ContextTypes

ADMIN_IDS = {int(i) for i in os.getenv("TELEGRAM_ADMIN_IDS", "").split(',') if i}
REPORT_IDS = [int(i) for i in os.getenv("TELEGRAM_REPORT_IDS", "").split(',') if i]
BAN_THRESHOLD = int(os.getenv("BAN_THRESHOLD", 3))
BAN_TIME = int(os.getenv("BAN_TIME", 3600))

_attempts: dict[int, tuple[int, float]] = {}

async def is_authorized(update: Update) -> bool:
    uid = update.effective_user.id
    if uid in _attempts and _attempts[uid][1] > time.time():
        return False
    if uid in ADMIN_IDS:
        _attempts.pop(uid, None)
        return True
    cnt, _ = _attempts.get(uid, (0, 0))
    cnt += 1
    if cnt >= BAN_THRESHOLD:
        _attempts[uid] = (cnt, time.time() + BAN_TIME)
    else:
        _attempts[uid] = (cnt, 0)
    return False

