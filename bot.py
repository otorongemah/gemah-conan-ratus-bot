"""
    GEMAH CONAN RATUS - BOT: Multiplatform bot for both Telegram and Discord
    By Gemah Otorongoso - 2020

    This bot is not under any particular license, but it is still an opensource project.
    It may be used as it is, as long as you tweak it enough for it to be your own bot.
    Please do not use it as your own private bot.
    
    Extensions/Libraries used:
     - python-dotenv (https://pypi.org/project/python-dotenv/)
     - python-telegram-bot (https://github.com/python-telegram-bot/python-telegram-bot)
"""

import logging
import os
import random

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

# Prepare logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Load data from the environment and prepare the bot to run
load_dotenv()

GREETINGS_TO_RESPOND_LIST = os.getenv("GREETING_WORDS").split("|")
GREETINGS_RESPONSE_LIST = os.getenv("BOT_GREETINGS").split("|")

# Functions


def generic_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


def telegram_start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="H-Hello there. My n-name is Conan. Nice to meet you. \U0001F42D \U0001F4A6")


def greeting_response(update, context):
    response = random.choice(GREETINGS_RESPONSE_LIST)

    if response == "EMOJI_REPLY":
        response = "\U0001F42D\U0001F4A6\U0001F4A6"

    context.bot.send_message(chat_id=update.effective_chat.id, text=response)


def temperature_response(update, context):  # TODO: fix value parsing
    response = ""
    temperature = context.args

    if not temperature:
        response = "I need a temperature value to work with..."
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=response)
    elif ~isinstance(temperature, (int, float)):
        response = "I can't work with something that is not a number!"
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=response)
    else:
        actual_temp = float(temperature)
        temp_keyboard = [InlineKeyboardButton("C to F", callback_data=(1, actual_temp)),
                         InlineKeyboardButton("F to C", callback_data=(2, actual_temp))]
        reply_keyboard_markup = InlineKeyboardMarkup(temp_keyboard)
        update.message.reply_text("Please choose one option:",
                                  reply_markup=reply_keyboard_markup)


# Commands and other handling


# Init
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Start
start_handler = CommandHandler('start', telegram_start)
dispatcher.add_handler(start_handler)

# Temperature
temperature_handler = CommandHandler('temperature', temperature_response)
dispatcher.add_handler(temperature_handler)

# Greeting handling
greeting_handler = MessageHandler(Filters.text(GREETINGS_TO_RESPOND_LIST) & (~Filters.command),
                                  greeting_response)
dispatcher.add_handler(greeting_handler)

# Run the bot
updater.start_polling()
updater.idle()
