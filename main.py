import os
import telebot
from flask import Flask
from threading import Thread

# 1. Web Server Setup (Render ko online rakhne ke liye)
app = Flask('')

@app.route('/')
def home():
    return "Bot is running online!"

def run():
    # Render hamesha port 10000 mangta hai
    app.run(host='0.0.0.0', port=10000)

# 2. Telegram Bot Setup
# Aapka naya token niche hai
TOKEN = "8530619211:AAEYmu7aIFaBgwqO3LBLt6E21x3aQQHri3o"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Namaste! Main naye setup (Render) par chalu ho gaya hoon. ✅")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Aapne kaha: " + message.text)

# 3. Dono ko ek sath chalane ke liye
if __name__ == "__main__":
    # Server ko background mein chalayein
    t = Thread(target=run)
    t.start()
    
    print("Bot is starting now...")
    # Bot ko polling par lagayein
    bot.infinity_polling()
  
