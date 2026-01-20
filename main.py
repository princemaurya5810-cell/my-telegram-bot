import os
import telebot
import random
from telebot import types
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Vichar Bot is Active!"

def run():
    app.run(host='0.0.0.0', port=10000)

# TOKEN check karein:
TOKEN = '8530619211:AAEYmu7aIFaBgwqO3LBLt6E21x3aQQHri3o'
bot = telebot.TeleBot(TOKEN)

vichar_data = [
    {"topic": "Science 🔬", "content": "प्रकाश (Light) को सूर्य से पृथ्वी तक पहुँचने में लगभग 8 मिनट 20 सेकंड लगते हैं।"},
    {"topic": "Philosophy 💡", "content": "'अपरीक्षित जीवन जीने योग्य नहीं है।' - सुकरात"},
    {"topic": "Politics ⚖️", "content": "लोकतंत्र का अर्थ केवल वोट देना नहीं, बल्कि सही सवाल पूछना भी है।"},
    {"topic": "Technology 💻", "content": "Quantum Computers भविष्य में आज के सुपर कंप्यूटर से हज़ारों गुना तेज़ होंगे।"}
]

quiz_data = [
    {"q": "भारत का संविधान कब लागू हुआ?", "o": ["1947", "1950", "1952"], "c": 1},
    {"q": "किस ग्रह को 'लाल ग्रह' कहा जाता है?", "o": ["शुक्र", "मंगल", "बृहस्पति"], "c": 1}
]

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('आज का विचार 💡')
    btn2 = types.KeyboardButton('नया Quiz खेलें 🧠')
    btn3 = types.KeyboardButton('YouTube Updates 📺')
    markup.add(btn1, btn2, btn3)
    
    bot.send_message(message.chat.id, f"नमस्ते {message.from_user.first_name}! 'Vichar' Bot में आपका स्वागत है।", reply_markup=markup)

@bot.message_handler(commands=['add'])
def add_vichar(message):
    msg = bot.reply_to(message, "नया विचार इस तरह भेजें: Topic | Content")
    bot.register_next_step_handler(msg, save_vichar)

def save_vichar(message):
    try:
        parts = message.text.split('|')
        if len(parts) == 2:
            vichar_data.append({"topic": parts[0].strip(), "content": parts[1].strip()})
            bot.reply_to(message, "✅ नया विचार सुरक्षित!")
        else:
            bot.reply_to(message, "❌ Format: Topic | Content")
    except:
        bot.reply_to(message, "❌ Error!")

@bot.message_handler(func=lambda m: True)
def handle_msg(message):
    # Yahan text bilkul button se match hona chahiye
    if message.text == 'आज का विचार 💡':
        item = random.choice(vichar_data)
        bot.send_message(message.chat.id, f"📑 *विषय:* {item['topic']}\n\n{item['content']}", parse_mode="Markdown")
    
    elif message.text == 'नया Quiz खेलें 🧠':
        quiz = random.choice(quiz_data)
        bot.send_poll(message.chat.id, quiz['q'], quiz['o'], type='quiz', correct_option_id=quiz['c'], is_anonymous=False)
    
    elif message.text == 'YouTube Updates 📺':
        bot.send_message(message.chat.id, "🎥 *Latest Updates:* https://youtube.com/@vicharwithayush")

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    # skip_pending=True se purana "Red Error" nahi aayega
    bot.infinity_polling(skip_pending=True)
    
