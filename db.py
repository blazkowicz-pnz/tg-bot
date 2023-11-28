import telebot
import sqlite3

TOKEN = "6929195675:AAGoFJ-XBZCPvb-0tF7-d-cj3meftxogqCc"
bot = telebot.TeleBot(TOKEN)
name = ''

@bot.message_handler(commands=["start"])
def start(message):
    conn = sqlite3.connect("test.sql")
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS user(id int auto_increment primary key, name varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, "Hello, i'll register you now, Enter your name!")
    bot.register_next_step_handler(message, username)


def username(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, "Enter password")
    bot.register_next_step_handler(message, user_pass)


def user_pass(message):
    password = message.text.strip()
    conn = sqlite3.connect("test.sql")
    cur = conn.cursor()
    cur.execute('INSERT INTO user (name, pass) VALUES ("%s", "%s")' % (name, password))
    conn.commit()
    cur.close()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("User list", callback_data="user_list"))
    bot.send_message(message.chat.id, "User registered", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    user_info = ''
    conn = sqlite3.connect('test.sql')
    cur = conn.cursor()
    cur.execute("SELECT * FROM user")
    users = cur.fetchall()
    for user in users:
        user_info += f"Name: {user[1]}, Password: {user[2]}\n"
    cur.close()
    conn.close()
    bot.send_message(call.message.chat.id, user_info)


bot.polling(none_stop=True)