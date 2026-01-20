import os
import telebot
from telebot import types
from flask import Flask
from threading import Thread

# 1. Render ko online rakhne ke liye Web Server
app = Flask('')

@app.route('/')
def home():
    return "Vichar Bot is Online!"

def run():
    app.run(host='0.0.0.0', port=10000)

# 2. Telegram Bot Setup
TOKEN = '8530619211:AAEYmu7aIFaBgwqO3LBLt6E21x3aQQHri3o'
bot = telebot.TeleBot(TOKEN)

# Start Command
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('Daily Vichar (Science/Philosophy) 💡')
    btn2 = types.KeyboardButton('Brain Quiz 🧠')
    btn3 = types.KeyboardButton('YouTube Updates 📺')
    btn4 = types.KeyboardButton('Contact Admin ✉️')
    markup.add(btn1, btn2, btn3, btn4)
    
    welcome_text = (
        "नमस्ते आयुष! 'Vichar' Bot में आपका स्वागत है। 🙏\n\n"
        "यहाँ आपको Science, Technology, Philosophy और Politics पर रोज़ाना नए विचार मिलेंगे।"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# Button Handlers
@bot.message_handler(func=lambda m: True)
def handle_msg(message):
    if message.text == 'Daily Vichar (Science/Philosophy) 💡':
        # Yahan aap roz naya text dal sakte hain
        vichar_text = (
            "🚀 *Aaj Ka Vichar:*\n\n"
            "*Science:* Quantum Entanglement ke mutabik do kan (particles) lakho light years door hokar bhi ek dusre se jude ho sakte hain.\n\n"
            "*Philosophy:* Socrates ne kaha tha, 'Main sirf itna jaanta hoon ki main kuch nahi jaanta.'\n\n"
            "Aapka kya sochna hai? @vicharwithayush par batayein!"
        )
        bot.send_message(message.chat.id, vichar_text, parse_mode="Markdown")

    elif message.text == 'Brain Quiz 🧠':
        bot.send_poll(
            message.chat.id, 
            "Prakash (Light) ki speed kya hai?", 
            ["1 Lakh km/s", "3 Lakh km/s", "5 Lakh km/s"], 
            type='quiz', 
            correct_option_id=1, 
            is_anonymous=False
        )

    elif message.text == 'YouTube Updates 📺':
        update_text = (
            "🎥 *Latest from @vicharwithayush:*\n\n"
            "Naya video dekhne ke liye niche link par click karein:\n"
            "https://youtube.com/@vicharwithayush"
        )
        bot.send_message(message.chat.id, update_text, parse_mode="Markdown")

    elif message.text == 'Contact Admin ✉️':
        bot.send_message(message.chat.id, "📧 Sampark karein: @vicharwithayush")

# 3. Bot chalane ka logic
if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    print("--- VICHAR BOT IS NOW LIVE ON RENDER! ---")
    bot.infinity_polling()

