# -*- coding: utf-8 -*-
"""
Created on Sat Mar 03 13:22 2018
@author: IrinaZakharova
"""

# -*- coding: utf-8 -*-

import telebot
from telebot import types
import requests
import pictures_config as config
import boto3


bot = telebot.TeleBot(config.token)

# Начало диалога
# По команде /reset будем сбрасывать состояния, возвращаясь к началу диалога

@bot.message_handler(commands=["start","reset"], content_types=['text'])
def cmd_reset(message):
    bot.send_message(message.chat.id, "Приветствую! Может, хотя бы в этот раз побегаю и разомнусь,ноги затекли")
    bot.send_message(message.chat.id, "(не обращай внимание на мои мысли вслух, лучше пришли ЛЮБОЙ ТЕКСТ, я жду)")

@bot.message_handler(content_types=['text'])
def user_entering_name(message):
    bot.send_message(message.chat.id, "Что ж, давай, я спрячу твоё фото, никто не найдет!")
    bot.send_message(message.chat.id, "...Кроме нас, конечно же ;)")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Да", callback_data="да"))
    markup.add(types.InlineKeyboardButton(text="Нет", callback_data="нет"))
    bot.send_message(message.chat.id,"Ну что, хочешь дать мне поручение? :)", reply_markup = markup)

    
@bot.message_handler(content_types=['photo'])
def user_picture(message):
    bot.send_message(message.chat.id, "Подожди немного, скоро вернусь и расскажу, где спрятал твое фото!")
    file_info = bot.get_file(message.photo[len(message.photo)-1].file_id)
    bot.send_message(message.chat.id, "Шаг 1/5: Я получил file_path = {0}".format(file_info.file_path))

    """api_url = 'https://api.telegram.org/file/bot{0}/{1}'.format(config.token, file_info.file_path)
    bot.send_message(message.chat.id, "Шаг 3/3: ссылка на твой файл => {0}".format(api_url))
    !!!ВЫШЕ ==> ПОЧЕМУ-ТО НЕ РАБОТАЕТ, ПОПРОБУЕМ ВЫВЕСТИ ССЫЛКУ ИЗ S3
    !!!НИЖЕ ==> НАДО РАЗБИРАТЬСЯ, КАК СОЗДАВАТЬ ДИРЕКТОРИИ...
    downloaded_file = bot.download_file(file_info.file_path)
    src = 'D://FinTech/Cloud_computing/Wakayama/{0}/{1}'.format(user,file_info.file_path)
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, "Фото добавлено")"""

    user = message.from_user.id
    bot.send_message(message.chat.id, "Шаг 2/5: Я получил user_id = {0}".format(user))

    s3 = boto3.resource('s3')
    bot.send_message(message.chat.id, "Подключился к облаку")
    file_name=file_info.file_path
    bucket_name="wakayama13"
    bucket=s3.Bucket(bucket_name)

    for object in bucket.objects.all():
        if object.key == "{0}/{1}".format(user,file_name[:6]):
            bucket.upload_file(Filename=file_name, Key="{0}/{1}".format(user, file_name))
        else:
            bucket.put_object(Key="{0}/{1}".format(user,file_name[:6]))
            bucket.upload_file(Filename=file_name,Key="{0}/{1}".format(user,file_name))

    
    bot.send_message(message.chat.id, "Шаг 3/5: Я загрузил файл в облако")
    s3_url="{0}/{1}/{2}".format(config.endpoint, Bucket=bucket_name, Key="{0}/{1}".format(user,file_name))
    bot.send_message(message.chat.id, "Шаг 4/5: Лови ссылку => {0}".format(s3_url))

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Да", callback_data="да"))
    markup.add(types.InlineKeyboardButton(text="Нет", callback_data="нет"))
    bot.send_message(message.chat.id, "Ну что, хочешь дать мне еще одно поручение? :)", reply_markup=markup)


    """result = []
    result.append(user)
    print(result)

    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Нажми и увидишь своё фото", url=)
    keyboard.add(url_button)
    bot.send_message(message.chat.id, "Ну, вот и все, твое фото лежит тут! быстро, не правда ли :)", reply_markup=keyboard)
    """


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    if call.message:
        if call.data == "да":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Отлично! Присылай фото и ничего, кроме фото!")

        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Жаль, тогда попробуем в следующий раз (напиши мне /reset, я жду)")




if __name__ == '__main__':
    bot.polling(none_stop=True)