import telebot
from telebot import types

api_token = '5526842178:AAHFQdi4fkO6i9Y66AfyegmjQVd-NdWX1cg'

bot = telebot.TeleBot(api_token)

request_dict = {}


def main(mess, key):
    message_arr = list()
    for x in mess:
        message_arr.append((ord(x)))
    main_arr = list()
    for i in range(len(message_arr)):
        main_arr.append(message_arr[i] ^ int(key))
    result = ''
    for char in main_arr:
        result += chr(int(char))
    return result


@bot.message_handler(commands=['help', 'start'])
def start(message):
    url = '[исключащего ИЛИ](https://w.wiki/5GTh)'
    user_name = message.from_user.username
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton('Начать')
    markup.add(btn)
    bot.send_message(message.chat.id, f'👋🏻 Привет\! @{user_name} \n Я \- Бот, выполняющий шифрование/дешифрование сообщений, '
                                    f'основанное на операции {url}\.', reply_markup=markup, parse_mode='MarkdownV2', disable_web_page_preview=True)


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    if message.text == 'Начать':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Шифрование')
        btn2 = types.KeyboardButton('Дешифрование')
        markup.add(btn1, btn2)
        msg = bot.send_message(message.chat.id, 'Выберите нужное преобразование', reply_markup=markup)
        bot.register_next_step_handler(msg, process_choose_step)


def process_choose_step(message):
    if message.text is not None:
        if message.text.lower() == 'шифрование' or message.text.lower() == 'дешифрование':
            request_dict['choose'] = message.text.lower()
            if message.text.lower() == 'шифрование':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn = types.KeyboardButton('Вернуться назад')
                markup.add(btn)
                msg = bot.send_message(message.chat.id, 'Введите сообщение для шифрования',reply_markup=markup)
                bot.register_next_step_handler(msg, process_mess_step)
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn = types.KeyboardButton('Вернуться назад')
                markup.add(btn)
                msg = bot.send_message(message.chat.id, 'Введите зашифрованное сообщение', reply_markup=markup)
                bot.register_next_step_handler(msg, process_mess_step)
        else:
            bot.send_message(message.chat.id, 'Неверный ввод')
            msg = bot.send_message(message.chat.id, 'Выберите нужное преобразование')
            bot.register_next_step_handler(msg, process_choose_step)


def process_mess_step(message):
    if message.text == 'Вернуться назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Шифрование')
        btn2 = types.KeyboardButton('Дешифрование')
        markup.add(btn1, btn2)
        msg = bot.send_message(message.chat.id, 'Выберите нужное преобразование', reply_markup=markup)
        bot.register_next_step_handler(msg, process_choose_step)
    else:
        request_dict['message'] = message.text
        msg = bot.send_message(message.chat.id, 'Введите ключ')
        bot.register_next_step_handler(msg, process_key_step)


def process_key_step(message):
    if message.text == 'Вернуться назад':
        if request_dict['choose'] == 'шифрование':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn = types.KeyboardButton('Вернуться назад')
            markup.add(btn)
            msg = bot.send_message(message.chat.id, 'Введите сообщение для шифрования', reply_markup=markup)
            bot.register_next_step_handler(msg, process_mess_step)
        if request_dict['choose'] == 'дешифрование':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn = types.KeyboardButton('Вернуться назад')
            markup.add(btn)
            msg = bot.send_message(message.chat.id, 'Введите зашифрованное сообщение', reply_markup=markup)
            bot.register_next_step_handler(msg, process_mess_step)
    elif message.text.isdigit():
        request_dict['key'] = message.text
        result = main(request_dict['message'], request_dict['key'])
        if result is not None:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn = types.KeyboardButton('Начать')
            markup.add(btn)
            if request_dict['choose'] == 'шифрование':
                bot.send_message(message.chat.id, f'Зашифрованный текст: {result}', reply_markup=markup)
            elif request_dict['choose'] == 'дешифрование':
                bot.send_message(message.chat.id, f'Расшифрованный текст: {result}', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Ошибка, попробуйте снова /start')
    else:
        bot.send_message(message.chat.id, 'Ключ должен быть числом')
        msg = bot.send_message(message.chat.id, 'Введите ключ')
        bot.register_next_step_handler(msg, process_key_step)


bot.polling(none_stop=True)