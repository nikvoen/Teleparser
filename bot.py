import time
import secrets
import string
import telebot
import pyautogui
from telebot import types
from datetime import datetime, timedelta
from dubnium import create_user, fix_errors


bot = telebot.TeleBot('api')


def PasswordGenerator():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(8))


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    newuser = types.KeyboardButton("Create user 🔐")
    check = types.KeyboardButton("Check errors 🔍")
    markup.add(newuser, check)
    bot.send_message(message.chat.id, "I am ready", reply_markup=markup)


@bot.message_handler(content_types='text')
def handler(message):
    if message.text == "Create user 🔐":
        tmp_msg = bot.send_message(message.chat.id, "Processing..")
        with open('D:/database/lastnumber.txt', 'r+') as file:
            login = str(int(file.read()) + 1)
            file.seek(0)
            file.truncate()
            file.write(login)
        login = f'Acc{login}'
        password = PasswordGenerator()
        result = create_user(login, password)

        attempts = 1

        while result == 2 and attempts <= 3:
            time.sleep(6)
            tmp_msg = bot.edit_message_text(f"Repeating.. {attempts}/3", tmp_msg.chat.id, tmp_msg.message_id)
            result = create_user(login, password)
            attempts += 1

        if result == 1:
            msg = f'Login: {login}\nPassword: {password}\nShared key: vpn\n'

            bot.edit_message_text("Success ✅", tmp_msg.chat.id, tmp_msg.message_id)
            bot.send_message(message.chat.id, msg)

            today = datetime.now()

            hour = int(time.strftime("%H", time.localtime()))

            if hour >= 20:
                file_date = today + timedelta(days=9)
            else:
                file_date = today + timedelta(days=8)

            file_date = '.'.join(file_date.strftime("%d %m").split())

            with open(f'D:/database/{file_date}.txt', 'a') as file:
                file.write(f'{login} {password}\n')

        elif result == 2:
            bot.edit_message_text("Error ❌", tmp_msg.chat.id, tmp_msg.message_id)

        else:
            bot.send_message(message.chat.id, result)

    if message.text == "Check errors 🔍":
        try:
            with open('D:/database/errors.txt', 'r') as file:
                types.ReplyKeyboardRemove()
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                markup.add(types.KeyboardButton("Display the list 🗂"),
                           types.KeyboardButton("Fix it ⚙"),
                           types.KeyboardButton("🔙"))
                bot.send_message(message.chat.id, "I found something", reply_markup=markup)

        except Exception:
            bot.send_message(message.chat.id, 'All is right! 👌')

    if message.text == "Display the list 🗂":
        with open('D:/database/errors.txt', 'r') as file:
            for line in file:
                bot.send_message(message.chat.id, line)

    if message.text == "Fix it ⚙":
        result = fix_errors()
        if result == 0:
            types.ReplyKeyboardRemove()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            markup.add(types.KeyboardButton("Create user 🔐"), types.KeyboardButton("Check errors 🔍"))
            bot.send_message(message.chat.id, "Success ✅", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "I have problems")

    if message.text == "🔙":
        types.ReplyKeyboardRemove()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton("Create user 🔐"), types.KeyboardButton("Check errors 🔍"))
        bot.send_message(message.chat.id, "I am ready", reply_markup=markup)


bot.infinity_polling()
