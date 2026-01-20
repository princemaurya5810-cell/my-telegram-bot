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

TOKEN = '8530619211:AAEYmu7aIFaBgwqO3LBLt6E21x3aQQHri3o'
bot = telebot.TeleBot(TOKEN)

# Aapki Admin ID (Yahan apni Telegram ID dalien agar pata ho, varna ye sabke liye khula rahega)
ADMIN_ID = None 

# --- Vichar aur Quiz ki Database ---
vichar_data = [
    {"topic": "Science 🔬", "content": "प्रकाश (Light) को सूर्य से पृथ्वी तक पहुँचने में लगभग 8 मिनट 20 सेकंड लगते हैं।"},
    {"topic": "Philosophy 💡", "content": "सुकरात ने कहा था, 'अपरीक्षित जीवन जीने योग्य नहीं है।'"},
    {"topic": "Politics ⚖️", "content": "असली लोकतंत्र वह है जहाँ समाज का सबसे कमज़ोर व्यक्ति भी सुरक्षित महसूस करे।"},
    {"topic": "Technology 💻", "content": "आने वाले समय में Quantum Computers आज के सबसे तेज़ सुपर कंप्यूटर से भी हज़ारों गुना तेज़ होंगे।"}
]

quiz_data = [
    {"q": "भारत का संविधान कब लागू हुआ?", "o": ["1947", "1950", "1952"], "c": 1},
    {"q": "किस ग्रह को 'लाल ग्रह' कहा जाता है?", "o": ["शुक्र", "मंगल", "बृहस्पति"], "c": 1},
    {"q": "दुनिया की सबसे लंबी नदी कौन सी है?", "o": ["Amazon", "Nile", "Ganga"], "c": 1}
]

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('आज का विचार 💡')
    btn2 = types.KeyboardButton('नया Quiz खेलें 🧠')
    btn3 = types.KeyboardButton('YouTube Updates 📺')
    markup.add(btn1, btn2, btn3)
    
    bot.send_message(message.chat.id, f"नमस्ते {message.from_user.first_name}! 'Vichar' Bot में आपका स्वागत है। \n\nनीचे दिए गए बटन दबाकर ज्ञान की यात्रा शुरू करें।", reply_markup=markup)

# --- Admin Feature: Naya Vichar Jodne Ke Liye ---
@bot.message_handler(commands=['add'])
def add_vichar(message):
    msg = bot.reply_to(message, "नया विचार इस तरह लिखें: Topic | Content\n(उदाहरण: Science | चाँद पृथ्वी से हर साल 3.8 cm दूर जा रहा है)")
    bot.register_next_step_handler(msg, save_vichar)

def save_vichar(message):
    try:
        parts = message.text.split('|')
        if len(parts) == 2:
            new_item = {"topic": parts[0].strip(), "content": parts[1].strip()}
            vichar_data.append(new_item)
            bot.reply_to(message, "✅ धन्यवाद! नया विचार सुरक्षित कर लिया गया है।")
        else:
            bot.reply_to(message, "❌ गलत फॉर्मेट! कृपया 'Topic | Content' का पालन करें।")
    except Exception as e:
        bot.reply_to(message, "❌ कुछ गड़बड़ हुई।")

@bot.message_handler(func=lambda m: True)
def handle_msg(message):
    if message.text == 'आज का विचार 💡':
        item = random.choice(vichar_data)
        text = f"📑 *विषय:* {item['topic']}\n\n{item['content']}"
        bot.send_message(message.chat.id, text, parse_mode="Markdown")
    
    elif message.text == 'नया Quiz खेलें 🧠':
        quiz = random.choice(quiz_data)
        bot.send_poll(message.chat.id, quiz['q'], quiz['o'], type='quiz', correct_option_id=quiz['c'], is_anonymous=False)
    
    elif message.text == 'YouTube Updates 📺':
        bot.send_message(message.chat.id, "🎥 *Latest Video from @vicharwithayush:*\n\nhttps://youtube.com/@vicharwithayush", parse_mode="Markdown")

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.infinity_polling(skip_pending=True)


    
