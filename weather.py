import telebot
import requests
import json

TOKEN = "6929195675:AAGoFJ-XBZCPvb-0tF7-d-cj3meftxogqCc"
API = "db3be74615bc9d0ce16fb299335490cd"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Hello! Name your city, please!")


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric")
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data['main']['temp']
        bot.reply_to(message, f"weather now: {temp}")

        image = 'sun.jpg' if temp > 5.0 else 'snow.jpg'
        file = open('images/' + image, 'rb')
        bot.send_photo(message.chat.id, file)
    else:
        bot.reply_to(message, "city  not found!!!!")




bot.polling(none_stop=True)