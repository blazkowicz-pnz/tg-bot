import telebot
from currency_converter import CurrencyConverter
from telebot import types



TOKEN = "6929195675:AAGoFJ-XBZCPvb-0tF7-d-cj3meftxogqCc"

bot = telebot.TeleBot(TOKEN)
currency = CurrencyConverter()
amount = 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello! Enter sum")
    bot.register_next_step_handler(message, summa)


def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Invalid sum format')
        bot.register_next_step_handler(message, summa)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton("USD/EUR", callback_data="usd/eur")
        btn2 = types.InlineKeyboardButton("EUR/USD", callback_data="eur/usd")
        btn3 = types.InlineKeyboardButton("USD/GBR", callback_data="usd/gbr")
        btn4 = types.InlineKeyboardButton("other", callback_data="else")
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, "select a pair", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'The number should be higher ZERO, Enter correct sum')
        bot.register_next_step_handler(message, summa)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != "else":
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f"Result: {round(res, 2)}. You can enter amount again")
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, "Enter pair ")
        bot.register_next_step_handler(call.message, my_currency)


def my_currency(message):
    try:
        values = message.text.upper().split("/")
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f"Result: {round(res, 2)}. You can enter amount again")
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, "invalid format, enter correct summ")
        bot.register_next_step_handler(message, my_currency)



bot.polling(none_stop=True)