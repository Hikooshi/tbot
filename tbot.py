import telebot
import requests
from bs4 import BeautifulSoup
import re
from config import token

bot = telebot.TeleBot(token)
programs = {}

@bot.message_handler(commands=["getAll"])
def get_text_messages(message):
    global programs
    response = requests.get("https://pastebin.com/u/Hikooshi").text
    soup = BeautifulSoup(response, "lxml")
    block = soup.find("table")
    name = block.find_all("a")
    ptrn = re.compile(r"\w+")
    kb = telebot.types.InlineKeyboardMarkup()
    buttonList = []
    for i in range(0, len(name), 2):
        pName = name[i].getText()
        slc = str(name[i])[10:]
        fptrn = ptrn.search(slc).group()
        programs[pName] = fptrn
        kb.add(telebot.types.InlineKeyboardButton(text=pName, url="https://pastebin.com/raw/" + fptrn))

    bot.send_message(message.from_user.id, "Выберите программу", reply_markup=kb)

bot.infinity_polling()1