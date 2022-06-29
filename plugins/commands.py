


import os
import time
import psutil
import shutil
import string
import asyncio
from pyrogram import Client, filters
from asyncio import TimeoutError
from pyrogram.errors import MessageNotModified
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, ForceReply
from plugins.config import Config
from plugins.script import Translation
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from plugins.database.add import add_user_to_database
from plugins.functions.forcesub import handle_force_subscribe

@Client.on_message(filters.command(["start"]) & filters.private)
async def start(bot, update):
    if not update.from_user:
        return await update.reply_text("😬 Something went wrong with your profile at telegram or Pyrogram side.")
    await add_user_to_database(bot, update)
    await bot.send_message(
        Config.LOG_CHANNEL,
           f"#NEW_USER: \n\nNew User [{update.from_user.first_name}](tg://user?id={update.from_user.id}) started @{Config.BOT_USERNAME} !!"
    )
    
    if Config.UPDATES_CHANNEL:
      fsub = await handle_force_subscribe(bot, update)
      if fsub == 400:
        return
    await update.reply_text(
        text=Translation.START_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=Translation.START_BUTTONS
    )


@Client.on_message(filters.command(["rate"]) & filters.private)
async def rate(bot, update):
            await bot.forward_messages(update.chat.id, "@Super_botz", Config.RATE_MSG_ID)
        
@Client.on_message(filters.command(["me"]) & filters.private)
async def me(bot, update):
  try:
    await bot.send_message(
              chat_id=update.chat.id,
              text="Telegram ID : {}".format(update.from_user.id),
              parse_mode="html",
              disable_web_page_preview=True
    )
  except Exception as e:
    await update.reply_text(str(e))
