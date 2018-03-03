# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 14:20 2018
@author: Bulat

Updated on Sat Mar 03 13:22 2018
@author: IrinaZakharova
"""

# -*- coding: utf-8 -*-

import telebot
from telebot import types
import dbworker
import os
import requests
from vedis import Vedis
from enum import Enum

token = '548774974:AAHW4F5trZ5tQ1bydKPvAmVYGbd4i1gPDis'
bot = telebot.TeleBot(token)
db_file = "pictures.vdb"

class States(Enum):
    """
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
    S_START = "0"  # Начало нового диалога
    S_DECIDE = "1"
    S_SEND_PIC = "2"

# Пытаемся узнать из базы «состояние» пользователя
def get_current_state(user_id):
    with Vedis(db_file) as db:
        try:
            return db[user_id]
        except KeyError:  # Если такого ключа почему-то не оказалось
            return States.S_START.value  # значение по умолчанию - начало диалога

path=os.getcwd()

# Начало диалога


@bot.message_handler(commands=["start"], content_types=['text'])
def cmd_start(message):
    state = get_current_state(message.chat.id)
    if state == States.S_DECIDE.value:
        markup = types.ReplyKeyboardMarkup()
        markup.row('Да', 'Нет')
        bot.send_message(message.chat.id, "Ну что, дашь мне поручение? :)", reply_markup=markup)
    elif state == States.S_SEND_PIC.value:
        bot.send_message(message.chat.id, "Я все еще жду фото... Не медли, я на низком старте :)")
    else:  # Под "остальным" понимаем состояние "0" - начало диалога
        bot.send_message(message.chat.id, "Привет! Давай я спрячу твое фото ;)")
        dbworker.set_state(message.chat.id, States.S_DECIDE.value)


# По команде /reset будем сбрасывать состояния, возвращаясь к началу диалога
@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    bot.send_message(message.chat.id, "С возвращением! Может, хотя бы в этот раз побегаю и разомнусь,ноги затекли")
    dbworker.set_state(message.chat.id, States.S_DECIDE.value)


@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == States.S_DECIDE.value)
def user_entering_name(message):
    # В случае с именем не будем ничего проверять, пусть хоть "25671", хоть Евкакий
    bot.send_message(message.chat.id, "Отличное имя, запомню! Загружай картинку!")
    dbworker.set_state(message.chat.id, config.States.S_SEND_PIC.value)



    
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_SEND_PIC.value, content_types=['photo'])
def user_picture(message):
    # В 67случае с именем не будем ничего проверять, пусть хоть "25671", хоть Евкакий
    bot.send_message(message.chat.id, "Загрузил! Давай ещё картинки!")
    print ('message.photo =', message.photo)
    fileID = message.photo[-1].file_id
    print ('fileID =', fileID)
    file = bot.get_file(fileID)
    print ('file.file_path =', file.file_path)
    telegram_api='http://api.telegram.org/file/bot497478839:AAFSeEOPFU2PGgBMYm_zSoZz8ez7s6-mWiE/photos/'
    long_url=os.path.join(telegram_api, file.file_path.rsplit('/',1)[-1])
    print(long_url)
    #image = urllib.URLopener()
    #image.retrieve(long_url,"00000001.jpg")
    with open(file.file_path.rsplit('/', 1)[-1], 'wb') as handle:
        response = requests.get(long_url, stream=True)

        if not response.ok:
            print (response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)
    user = message.from_user
    result = [user , long_url]
    print(result)

    #подключаем бота к S3
    import boto3
    s3 = boto3.resource('s3')

    """img = cv2.imread(long_url,0)
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()"""
    
    

    #plt.imshow(mpimg.imread(long_url))
    #display(Image(filename=long_url))
    
    
    
    #cv2.imwrite(os.path.join(path , 'waka.jpg'), message)
    #cv2.waitKey(0)

    dbworker.set_state(message.chat.id, config.States.S_SEND_PIC.value)
"""

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_KOFE.value)
def user_entering_coffee(message):
    # А вот тут сделаем проверку
    # На данном этапе мы уверены, что message.text можно преобразовать в число, поэтому ничем не рискуем
    if str(message.text) not in ('раф','американо','эспрессо','мокко','латте','Раф','Американо','Эспрессо','Мокко','Латте'):
        bot.send_message(message.chat.id, "Какой-то странный кофе. В нашем меню такого пока нет! Пожалуйста, выбери из списка: раф, латте, эспрессо, мокко, американо")
        return
    else:
        # Возраст введён корректно, можно идти дальше
        bot.send_message(message.chat.id, "Отлично, твой кофе уже готовится! Твой кофе стоит 100 рублей. Твой заказ №"+ str(np.random.randint(1, 10000 + 1)) + "! Ты можешь оплатить наличными либо переводом через Сбербанк Онлайн. Выбери способ оплаты")
        dbworker.set_state(message.chat.id, config.States.S_SET_PAYMENT.value)
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_SET_PAYMENT.value)
       
def user_entering_payment(message):
    # А вот тут сделаем проверку
    # На данном этапе мы уверены, что message.text можно преобразовать в число, поэтому ничем не рискуем
    if str(message.text) not in ('наличными','переводом','наличные','перевод', 'Наличными','Переводом','Наличные','Перевод'):
        bot.send_message(message.chat.id, "Я принимаю платежи пока только либо наличными, либо переводом. Пожалуйста, выбери способ еще раз")
        return
    elif str(message.text) in ('наличными','наличные', 'Наличными','Наличные'):
        bot.send_message(message.chat.id, "Отлично, запомни номер своего заказа! Я тебе напишу, когда кофе будет готов! Если захочешь ещё кофе - отправь команду /kofe.")
        dbworker.set_state(message.chat.id, config.States.S_START.value)

    elif str(message.text) in ('переводом','перевод', 'Переводом','Перевод'):
        bot.send_message(message.chat.id, "Отлично, номер карты для перевода 5555 5555 5555 5555!При оплате переводом ОБЯЗАТЕЛЬНО напиши в комментариях к переводу номер своего заказа! Я тебе напишу, когда кофе будет готов! Если захочешь ещё кофе - отправь команду /kofe.")
        dbworker.set_state(message.chat.id, config.States.S_START.value)


    
"""
"""
# Простейший инлайн-хэндлер для ненулевых запросов
@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(query):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="Нажми меня", callback_data="test"))
    results = []
    # Обратите внимание: вместо текста - объект input_message_content c текстом!
    single_msg = types.InlineQueryResultArticle(
        id="1", title="Press me",
        input_message_content=types.InputTextMessageContent(message_text="Я – сообщение из инлайн-режима"),
        reply_markup=kb
    )
    results.append(single_msg)
    bot.answer_inline_query(query.id, results)
"""

if __name__ == '__main__':
    bot.polling(none_stop=True)