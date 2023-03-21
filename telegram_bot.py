import logging
import telegram
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, ContextTypes, MessageHandler
from pymongo import MongoClient
import os
import requests

class telegram_bot:
    TOKEN = "5731902474:AAHfTKKu7h8-WZv4BD4njJuISnFVPOGXWxg"

    def __init__(self):
        self.cluster = MongoClient("mongodb+srv://basicallyanotheradmin:Akshay17@cluster0.0akcrf5.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.cluster["SecurityDatabase"]
        self.UserData = self.db["UserData"]
        logging.basicConfig (
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
        )

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if(self.UserData.find_one({"tid" : update.effective_chat.id}) == None):
            await context.bot.send_message(chat_id = update.effective_chat.id, text = "Hi there! Welcome to SentinelBot, the companion bot to your home security system!")
            data = {"tid" : update.effective_chat.id, "alert" : 0}
            self.UserData.insert_one(data)
        else:     
            await context.bot.send_message(chat_id=update.effective_chat.id, text = "Welcome back again!")


    async def reply_keyboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        kb = [[telegram.KeyboardButton('/yes')],
            [telegram.KeyboardButton('/no')]]
        kb_markup = telegram.ReplyKeyboardMarkup(kb)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Discrepancy detected. Do you want to send alert?", reply_markup=kb_markup)


    async def yes(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Alert has been sent.")
        self.UserData.find_one({"tid": update.effective_chat.id}).update_one({"alert": 0}, {"alert": 1})

    async def no(slef, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Alert hasn't been sent.")


    def main(self):
        application = ApplicationBuilder().token(telegram_bot.TOKEN).build()
        start_handler = CommandHandler('start', self.start)
        reply_keyboard_handler = CommandHandler('reply_keyboard', self.reply_keyboard)
        yes_handler = CommandHandler('yes', self.yes)
        no_handler = CommandHandler('no', self.no)
        application.add_handler(start_handler)
        application.add_handler(reply_keyboard_handler)
        application.add_handler(yes_handler)
        application.add_handler(no_handler)
        application.run_polling()
        

bot = telegram_bot()
bot.main()