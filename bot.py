import telebot
from telebot import types
import requests
from flask import Flask

TOKEN = "8122568214:AAExyNrxhPOV1UUbMIdOL3EDKECaLq6X0lI"
bot = telebot.TeleBot(TOKEN)

# Flask hiyla usuli uchun
app = Flask(__name__)

# Majburiy kanal
CHANNEL_ID = "@kinolar_olami12346"  # E'tibor bering: "@" bilan yoziladi

# Kodlarga mos kinolar (qo'lda qo‘shib boriladi)
movies = {
    "70": "https://t.me/KINOLARtv07/1397",  # misol
    "72": "https://t.me/KINOLARtv07/1400",
    "71": "https://t.me/KINOLARtv07/1399",
    "66": "https://t.me/KINOLARtv07/1393",
    "67": "https://t.me/KINOLARtv07/1394",
    "68": "https://t.me/KINOLARtv07/1395",
    "69": "https://t.me/KINOLARtv07/1396",
    "65": "https://t.me/KINOLARtv07/1392",
    "64": "https://t.me/KINOLARtv07/1391",
    "63": "https://t.me/KINOLARtv07/1388",
    "62": "https://t.me/KINOLARtv07/1387",
    "61": "https://t.me/KINOLARtv07/1386",
    "60": "https://t.me/KINOLARtv07/1385",
    "59": "https://t.me/KINOLARtv07/1384",
    "58": "https://t.me/KINOLARtv07/1383",
    "57": "https://t.me/KINOLARtv07/1382",
    "56": "https://t.me/KINOLARtv07/1380",
    "55": "https://t.me/KINOLARtv07/1379",
    "40": "https://t.me/KINOLARtv07/1362",
    "41": "https://t.me/KINOLARtv07/1363",
    "42": "https://t.me/KINOLARtv07/1364",
    "43": "https://t.me/KINOLARtv07/1365",
    "44": "https://t.me/KINOLARtv07/1366",
    "45": "https://t.me/KINOLARtv07/1367",
    "46": "https://t.me/KINOLARtv07/1368",
    "47": "https://t.me/KINOLARtv07/1369",
    "48": "https://t.me/KINOLARtv07/1370",
    "49": "https://t.me/KINOLARtv07/1371",
    "50": "https://t.me/KINOLARtv07/1372",
    "51": "https://t.me/KINOLARtv07/1373",
    "52": "https://t.me/KINOLARtv07/1374",
    "53": "https://t.me/KINOLARtv07/1375",
    "54": "https://t.me/KINOLARtv07/1376",
    "39": "https://t.me/KINOLARtv07/1361",
    "38": "https://t.me/KINOLARtv07/1359",
    "37": "https://t.me/KINOLARtv07/1358",
    "36": "https://t.me/KINOLARtv07/1357",
    "35": "https://t.me/KINOLARtv07/1356",
    "34": "https://t.me/KINOLARtv07/1355",
    "33": "https://t.me/KINOLARtv07/1353",
    "32": "https://t.me/KINOLARtv07/1352",
    "31": "https://t.me/KINOLARtv07/1351",
    "30": "https://t.me/KINOLARtv07/1350",
    "29": "https://t.me/KINOLARtv07/1349",
    "28": "https://t.me/KINOLARtv07/1348",
    "27": "https://t.me/KINOLARtv07/1347",
    "26": "https://t.me/KINOLARtv07/1346",
    "25": "https://t.me/KINOLARtv07/1343",
    "24": "https://t.me/KINOLARtv07/1342",
    "23": "https://t.me/KINOLARtv07/1341",
    "22": "https://t.me/KINOLARtv07/1340",
    "21": "https://t.me/KINOLARtv07/1339",
    "73": "https://t.me/KINOLARtv07/1407",
    "74": "https://t.me/KINOLARtv07/1408",
    "75": "https://t.me/KINOLARtv07/1409",
    "76": "https://t.me/KINOLARtv07/1410",
    "77": "https://t.me/KINOLARtv07/1411",
    "78": "https://t.me/KINOLARtv07/1412",
    "79": "https://t.me/KINOLARtv07/1413",
    "80": "https://t.me/KINOLARtv07/1414"
}

# Flask index sahifa
@app.route('/')
def index():
    return "Bot ishlayapti!"

# Foydalanuvchi start bosganda
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    if check_subscription(user_id):
        bot.send_message(user_id, "🎬 Kino kodini yuboring:")
    else:
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("✅ Kanalga obuna bo‘lish", url=f"https://t.me/{CHANNEL_ID[1:]}")
        markup.add(btn)
        bot.send_message(user_id, "Botdan foydalanish uchun kanalga obuna bo‘ling!", reply_markup=markup)

# Kodni yozganda
@bot.message_handler(func=lambda message: True)
def send_movie(message):
    user_id = message.chat.id
    if not check_subscription(user_id):
        bot.send_message(user_id, "Avval kanalga obuna bo‘ling.")
        return

    code = message.text.strip()
    if code in movies:
        bot.send_message(user_id, f"Kino: {movies[code]}")
    else:
        bot.send_message(user_id, "❌ Bunday kod topilmadi.")

# Obuna bo‘lganligini tekshiruvchi funksiya
def check_subscription(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'creator', 'administrator']
    except:
        return False

# Botni Flask orqali ishga tushiramiz
import threading
def run_bot():
    bot.infinity_polling()

threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)