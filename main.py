# Импортирование всех файлов
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import executor
import string
import json
from pleyer import pleyers
import client
from text import open_file_txt, main, find_word, finish_spisok, add_pleyer_in_spisok

# Создание объектов бота и диспетчера
bot = Bot(token=client.token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Обьявление переменых
pleyers_last = 0  # мой айди
pleyer_1 = {}  # вспомогательная переменная для внесения имен и айди людей в базу данных
pleyer_vubor = []  # переменная для сохранения учасников игры
kol = 0
spisok_slov = ['Узнать результаты', 'Вернуться в меню', 'Информация о игре', 'Играть', 'Выйти из игры', 'Назад в меню',
               'Выбрать еще одного игрока', 'Начать игру', 'Информация о слове']
game_info = ''


# запись базы даных
async def write_file(pleyer_1):
    pleyer_temp =  await open_file()
    with open('pleyer_base.json', 'w') as f:
        pleyer_temp.update(pleyer_1)
        x = pleyer_temp
        json.dump(x, f)


async def open_file():
    with open('pleyer_base.json') as f:
        file = f.read()
        temp = json.loads(file)
    return temp


async def open_baze():
    with open('russian_nouns_with_definition.json', encoding="utf-8") as f:
        dict_baze = json.load(f)
    return dict_baze


async def slovo_information(slovo, message):
    about_slovo = await open_baze()
    await message.reply(about_slovo[slovo]['definition'], reply_markup= await keyboard_back())


async def slovo_information_2_0(slovo, message):
    about_slovo = await open_baze()
    await message.reply(about_slovo[slovo]['definition'], reply_markup=await keyboard_back())


# Удаляет уже выбраного игрока
async def kick_pleyer(pleyer_s):
    for i in pleyers_delet.items():
        if pleyer_s == i[1]:
            pleyer_vubor.append(i[1])
            pleyers_delet.pop(i[0])
            break


async def keyboard_rez():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_rez = types.KeyboardButton('Узнать результаты')
    button_men = types.KeyboardButton('Вернуться в меню')
    markup.add(button_rez, button_men)
    return markup


# Клавиатура меню
async def start_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_info = types.KeyboardButton('Информация о игре')
    button_game = types.KeyboardButton('Играть')
    button_slov = types.KeyboardButton('Толковый словарь')
    markup.add(button_game)
    markup.add(button_info)
    markup.add(button_slov)
    return markup


# Клавиатура на выход из игры
async def keyboard_bk():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_back = types.KeyboardButton('Выйти из игры')
    button_info = types.KeyboardButton('Информация о слове')
    markup.add(button_back, button_info)
    return markup

# Клавиатура для возращения
async def keyboard_back():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_back = types.KeyboardButton('Назад в меню')
    markup.add(button_back)
    return markup

# Клавиатура для добавления первого человека
async def keyboard_add_pleyers():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    d = []
    for key, value in pleyers_delet.items():
        key = types.KeyboardButton(value)
        d.append(key)
    return markup.add(*d)


# Клавиатура для добавления еще людей используеться на добавление 3 и более людей
async def last_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_pleyer = types.KeyboardButton('Выбрать еще одного игрока')
    button_game = types.KeyboardButton('Начать игру')
    markup.add(button_game)
    markup.add(button_pleyer)
    return markup


# Функция которая выводит кто следущий ходит
async def game_raz(pleyer_vubor, message):
    global kol
    if kol != len(pleyer_vubor) - 1:
        await message.reply(f'Сейчас ходит - {pleyer_vubor[kol]}')
        kol += 1
    elif kol == len(pleyer_vubor) - 1:
        await message.reply(f'Сейчас ходит - {pleyer_vubor[kol]}')
        kol = 0


async def game_raz_2_0(pleyer_vubor, message):
    global kol
    if kol - 1 != len(pleyer_vubor) - 1:
        await message.reply(f'Сейчас ходит - {pleyer_vubor[kol]}')
    elif kol - 1 == len(pleyer_vubor) - 1:
        await message.reply(f'Сейчас ходит - {pleyer_vubor[kol]}')


async def game_prov(pleyer_vubor, pleyer_name, chat_id):
    if pleyer_vubor[kol - 1] != pleyer_name:
        return False
    return True


async def information_game(message):
    for key, value in finish_spisok.items():
        await message.reply(f"У {key} - {len(value)} баллов", reply_markup= await keyboard_back())


# Фунцйия которая віводет на какую букву тебе надо написатьслово
async def next_word(message, pleyer_sms):
    global next_word_1
    if pleyer_sms[-1] == 'ь' or pleyer_sms[-1] == 'ъ':
        await message.reply(f"Тебе на '{pleyer_sms[-2]}'")
        next_word_1 = pleyer_sms[-2]
    else:
        await message.reply(f"Тебе на '{pleyer_sms[-1]}'")
        next_word_1 = pleyer_sms[-1]


# При нажатие старт твой id сохроняеться
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    pleyer_1[str(message.from_user.id)] = message.from_user.first_name.title()
    await write_file(pleyer_1)
    await message.reply(f'Привет {message.from_user.first_name}', reply_markup=await start_keyboard())


# При добавление человека он сохраняеться в базе данных
@dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def handler_new_member(message: types.Message):
    print(message)
    pleyer_1[message["new_chat_member"]["id"]] = message["new_chat_member"]["first_name"].title()
    await write_file(pleyer_1)
    await message.reply(f'Добро пожоловать в группу {message["new_chat_member"]["first_name"].title()}',
                     reply_markup=await start_keyboard())


# Основной код
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def get(message: types.Message):
    global pleyers_last, pleyers_delet, slovo, game_info, pleyer_vubor, world_back
    slovo = ''
    file_open = await open_file()
    txt_file = await open_file_txt()
    if message.text == 'Информация о игре':
        await message.reply('Это бот где ты можешь поиграть с друзьями в слова на последнюю букву.',
                         reply_markup=await keyboard_back())
    elif message.text == 'Назад в меню':
        await message.reply('Выберите пункт меню.', reply_markup=await start_keyboard())
        game_info = ''
    elif message.text == 'Толковый словарь':
        game_info = 'Толковый словарь'
        await message.reply('Напишите слово о котором вы хотите узнать информацию',
                         reply_markup=await keyboard_back())
    elif message.text not in spisok_slov and game_info == 'Толковый словарь':
        if message.text.strip(
                string.punctuation + " " + string.digits).lower() in txt_file:
            await slovo_information_2_0(message.text.strip(
                string.punctuation + " " + string.digits).lower(), message)
    elif message.text == 'Играть':
        world_back = []
        pleyer_vubor.append(message.from_user.first_name)
        pleyers_last = str(message.from_user.id)
        pleyers_delet = file_open
        pleyers_delet.pop(pleyers_last)
        if len(file_open) == 0:
            await message.reply('В группе не достаточно игроков')
        else:
            await message.reply('Выберите с кем вы хотите поиграть', reply_markup= await keyboard_add_pleyers())
    elif message.text in [*file_open.values()]:
        await message.reply('Выберите пункт меню.', reply_markup=await last_keyboard())
        await kick_pleyer(message.text)
    elif message.text == 'Выбрать еще одного игрока':
        if len(pleyers_delet) == 0:
            await message.reply('Больше игроков на выбор нету')
            await message.reply('Начните игру')
        else:
            await message.reply('Выберите с кем вы хотите поиграть', reply_markup= await keyboard_add_pleyers())
    elif message.text == 'Начать игру':
        await message.reply(f'Начинаем игру между - {", ".join(pleyer_vubor)}', reply_markup= await keyboard_bk())
        await add_pleyer_in_spisok(pleyer_vubor)
        await game_raz(pleyer_vubor, message)
        game_info = 'Начать игру' 
    elif message.text.strip( string.punctuation + " " + string.digits).lower() not in world_back and message.text not in spisok_slov and game_info == 'Начать игру':
        await game_prov(pleyer_vubor, message.from_user.first_name, message)
        if await game_prov(pleyer_vubor, message.from_user.first_name, message):
            if message.text.strip(string.punctuation + " " + string.digits).lower() in txt_file:
                if await main(message.text, message.from_user.first_name):
                    slovo = message.text.strip(string.punctuation + " " + string.digits).lower()
                    world_back.append(message.text.strip(string.punctuation + " " + string.digits).lower())
                    await game_raz(pleyer_vubor, message)
                    await next_word(message, message.text.strip(string.punctuation + " " + string.digits).lower())
            elif message.text not in txt_file:
                await message.reply('Такого слова несуществует')
                await message.reply( 'Игра закончена', reply_markup= await keyboard_rez())
                await message.reply(f'Проиграл - {message.from_user.first_name}', reply_markup= await keyboard_rez())
                pleyer_vubor = []
                game_info = ''
        else:
            await message.reply('Сейчас не твой ход')
            await game_raz_2_0(pleyer_vubor, message)
            await message.reply(f"Тебе на '{next_word_1}'")
    elif message.text.strip(string.punctuation + " " + string.digits).lower() in world_back and message.text not in spisok_slov:
        await message.reply('Такое слова уже вводили. Напишите другое')
    elif message.text == 'Узнать результаты':
        await information_game(message)
    elif message.text == 'Выйти из игры':
        pleyer_vubor = []
        game_info = ''
        await message.reply('Игра закончена', reply_markup= await keyboard_rez())
        await message.reply(f'{message.from_user.first_name} сдался', reply_markup= await keyboard_rez())
    elif message.text == 'Вернуться в меню':
        await message.reply('Выберите пункт меню.', reply_markup= await start_keyboard())   
    elif message.text == 'Информация о слове':
        if len(world_back) == 1:
            await slovo_information(world_back[0].strip(string.punctuation + " " + string.digits).lower(), message)
        if len(world_back) not in [0, 1]:
            await slovo_information(world_back[-2].strip(string.punctuation + " " + string.digits).lower(), message)
        else:
            await message.reply('Вы еще не написали слово', reply_markup= await keyboard_bk())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
