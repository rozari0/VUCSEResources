from pyrogram import filters
from pyrogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup

from bot import bot


@bot.on_message(filters.command("start"))
async def start(client, message):
    reply_markup = [
        [
            InlineKeyboardButton(text="Varsity Website", url="https://vu.edu.bd"),
            InlineKeyboardButton(text="Semesters", callback_data="homepage"),
        ],
    ]
    return await message.reply_photo(
        photo="https://i.ibb.co/F0rNmwV/cse.png",
        caption=f"Hello {message.from_user.first_name}, I'm here to find resources for VU CSE Depertment. I'm still in beta, so don't expect much.",
        reply_markup=InlineKeyboardMarkup(reply_markup),
    )


@bot.on_message(filters.command("credit"))
async def credit(_, message):
    text = "This bot is created by team NFSSD for CSE-34 Section B."
    return await message.reply_text(
        text=text,
    )


@bot.on_message(filters.command("help"))
async def credit(_, message):
    text = "**Help for VU CSE Resource Bot.**\n\n"
    text += "/start - Start This Bot.\n/semesters - Get all semesters.\n/help - Get this message\n/credit - Get info about the devoloper team."
    return await message.reply_text(
        text=text,
    )


@bot.on_callback_query(filters.regex(r"credit(.*?)"))
async def credit(_, query):
    text = "This bot is created by team NFSSD for CSE-34 Section B."
    reply_markup = [
        [
            InlineKeyboardButton(text="Semesters", callback_data="homepage"),
        ],
    ]
    return await query.message.edit(
        text=text,
        reply_markup=InlineKeyboardMarkup(reply_markup),
    )


@bot.on_message(filters.command("setcommands"))
async def start(app, _):
    await app.set_bot_commands(
        [
            BotCommand("start", "Start the bot."),
            BotCommand("semesters", "Get all semesters."),
            BotCommand("credit", "Show Devoloper Information."),
        ]
    )
