from aiogram import Bot, Dispatcher, executor, types
import logging
import notajaxparser as parser
from config import BOT_TOKEN
from sqlworker import SQLighter

bot_obj=Bot(token=BOT_TOKEN)
bot=Dispatcher(bot_obj)
db = SQLighter('db.db')
clear_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton(" "))
logging.basicConfig(level=logging.INFO)
menu=types.ReplyKeyboardMarkup(resize_keyboard=True)
button1=types.KeyboardButton("Узнать своё положение в таблице")
edBut1=types.KeyboardButton("Выбрать институт")
edBut2=types.KeyboardButton("Изменить номер")
menu.add(button1)
menu.row(edBut1,edBut2)


def generate_inline_selector():
    inline_kb = types.InlineKeyboardMarkup()
    inline_btn_1 = types.InlineKeyboardButton('Институт естественных наук и математики', callback_data='ienm')
    inline_btn_2 = types.InlineKeyboardButton('Институт новых материалов и технологий', callback_data='inmt')
    inline_btn_3 = types.InlineKeyboardButton('Институт радиоэлектроники и информационных технологий - РтФ', callback_data='rtf')
    inline_btn_4 = types.InlineKeyboardButton('Институт строительства и архитектуры', callback_data='isa')
    inline_btn_6 = types.InlineKeyboardButton('Институт физической культуры, спорта и молодежной политики', callback_data='ipe')
    inline_btn_7 = types.InlineKeyboardButton('Институт фундаментального образования', callback_data='ifo')
    inline_btn_8 = types.InlineKeyboardButton('Институт экономики и управления', callback_data='ieu')
    inline_btn_9 = types.InlineKeyboardButton('Уральский гуманитарный институт', callback_data='ugi')
    inline_btn_10 = types.InlineKeyboardButton('Уральский энергетический институт', callback_data='uei')
    inline_btn_11 = types.InlineKeyboardButton('Физико-технологический институт', callback_data='fti')
    inline_btn_12 = types.InlineKeyboardButton('Химико-технологический институт', callback_data='xti')
    inline_kb.add(inline_btn_1)
    inline_kb.add(inline_btn_2)
    inline_kb.add(inline_btn_3)
    inline_kb.add(inline_btn_4)
    inline_kb.add(inline_btn_6)
    inline_kb.add(inline_btn_7)
    inline_kb.add(inline_btn_8)
    inline_kb.add(inline_btn_9)
    inline_kb.add(inline_btn_10)
    inline_kb.add(inline_btn_11)
    inline_kb.add(inline_btn_12)
    return inline_kb


inline_kb=generate_inline_selector()


def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

@bot.message_handler(commands=['start'])
async def init_bot(message: types.Message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1=types.KeyboardButton("Начать узнавать своё положение!")
    markup.add(button1)
    if message.chat.username==None:
        name=message.chat.first_name
    else:
        name = message.chat.username
    if not db.user_exists(message.chat.id):
        db.add_user(message.chat.id,name)
    await message.answer("Привет 👋, я бот проверяющий ваше положение в конкурсном списке УРФУ среди тех, кто подал согласие.",reply_markup=markup)

@bot.message_handler(content_types=['text'])
async def get_text_messages(message):
    if message.chat.type=="private":
        if message.text == "Начать узнавать своё положение!" or message.text == "Изменить номер":
            if not db.user_exists(message.chat.id):
                db.add_user(message.chat.id,message.chat.username)
            db.update_status(message.chat.id,True)
            await message.answer("Введите ваш регистрационный номер:",reply_markup=clear_markup)
        elif message.text == "/help":
            await message.answer("Расскажу о метсте в рейниге или про ФИИТ /fiit.👺 Используй клваиатуру для управления.")
        elif message.text == "/fiit":
            await message.answer("ФИИТ - крута. @drannik_m рекомендует. https://fiit-urfu.ru")
        elif message.text == "Узнать своё положение в таблице":
            if not db.user_exists(message.chat.id):
                db.add_user(message.chat.id,message.chat.username)
            user=db.get_user(message.chat.id)
            print(user[5])
            if user[2]==None:
                await message.answer("Для начала выберите институт. ↙️ ")
            elif user[3] == None:
                await message.answer("Для начала измините номер. ↘️")
            else:
                await message.answer("🌐 Ищем вас в списках...")
                await message.answer(parser.get_abit_status(user[2],user[3]))
        elif message.text == "Выбрать институт":
            await message.answer("На какой институт вы подали согласие?", reply_markup=inline_kb)
        else:
            if not db.user_exists(message.chat.id):
                db.add_user(message.chat.id,message.chat.username)
            if db.get_user(message.chat.id)[4]:
                text=message.text.strip()
                if RepresentsInt(text):
                    db.update_fio(message.chat.id,text)
                    db.update_status(message.chat.id, False)
                    await message.answer( "👌 Ок.",reply_markup=menu)
                else:
                    await message.answer( "❌ Невалидный номер,попробуйте ещё раз.")
            else:
                await message.answer( "Я тебя не понимаю 😥. Используй клавиутру для управления")


@bot.callback_query_handler()
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    code = callback_query.data

    if not db.user_exists(callback_query.message.chat.id):
        db.add_user(callback_query.message.chat.id, callback_query.message.chat.username)
    if code=="ienm":
        db.update_inst(callback_query.message.chat.id,"Институт естественных наук и математики")
    elif code=="inmt":
        db.update_inst(callback_query.message.chat.id,"Институт новых материалов и технологий")
    elif code=="rtf":
        db.update_inst(callback_query.message.chat.id,"Институт радиоэлектроники и информационных технологий - РтФ")
    elif code=="isa":
        db.update_inst(callback_query.message.chat.id,"Институт строительства и архитектуры")
    elif code=="ipe":
        db.update_inst(callback_query.message.chat.id,"Институт физической культуры, спорта и молодежной политики")
    elif code=="ifo":
        db.update_inst(callback_query.message.chat.id,"Институт фундаментального образования")
    elif code=="ieu":
        db.update_inst(callback_query.message.chat.id,"Институт экономики и управления")
    elif code=="ugi":
        db.update_inst(callback_query.message.chat.id,"Уральский гуманитарный институт")
    elif code=="uei":
        db.update_inst(callback_query.message.chat.id,"Уральский энергетический институт")
    elif code=="fti":
        db.update_inst(callback_query.message.chat.id,"Физико-технологический институт")
    elif code=="xti":
        db.update_inst(callback_query.message.chat.id,"Химико-технологический институт")

    await bot_obj.edit_message_text(chat_id=callback_query.message.chat.id,message_id=callback_query.message.message_id,reply_markup=None,text="👌 Выбор зачтён!")
    await bot_obj.answer_callback_query(callback_query.id)


if __name__ == '__main__':
    executor.start_polling(bot, skip_updates=True)