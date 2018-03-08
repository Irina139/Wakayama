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
    file_info = bot.get_file(file_id)
    bot.send_message(message.chat.id, "Я получил file_id")
    api_url = 'https://api.telegram.org/file/bot{0}/{1}'.format(bot, file_info.file_path)
    #file = requests.get(api_url)
    user = message.from_user
    bot.send_message(message.chat.id, "URL = {0}".format(api_url))
    bot.send_message(message.chat.id, "File_id = {0}".format(file_info))

    s3 = boto3.client('s3')




    """result = []
    result.append(user)
    print(result)

    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Нажми и увидишь своё фото", url=)
    keyboard.add(url_button)
    bot.send_message(message.chat.id, "Ну, вот и все, твое фото лежит тут! быстро, не правда ли :)", reply_markup=keyboard)"""


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


    """!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #подключаем бота к S3
    s3 = boto3.resource('s3')
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"""



if __name__ == '__main__':
    bot.polling(none_stop=True)