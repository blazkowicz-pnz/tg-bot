from aiogram import Bot,Dispatcher,types,executor

TOKEN = "6929195675:AAGoFJ-XBZCPvb-0tF7-d-cj3meftxogqCc"

bot = Bot(TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # await bot.send_message(message.chat.id, "Hello")
    # await message.answer("Hello")
    await message.reply("ыыыыы")


@dp.message_handler(commands=["inline"])
async def info(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("site", url="google.com"))
    markup.add(types.InlineKeyboardButton("Hello", callback_data="хуй моржовый"))
    await message.reply("hello", reply_markup=markup)


@dp.callback_query_handler()
async def callback(call):
    await call.message.answer(call.data)



@dp.message_handler(commands=["reply"])
async def reply(message: types.Message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
    markup.add(types.KeyboardButton("Website1"))
    markup.add(types.KeyboardButton("Website2"))
    await message.answer("Hello", reply_markup=markup)

if __name__ == "__main__":
    executor.start_polling(dp)