# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 14:23:14 2018

@author: Bulat
"""


# -*- coding: utf-8 -*-
# Этот токен невалидный, можете даже не пробовать :)
import telebot


from enum import Enum

token = '548774974:AAHW4F5trZ5tQ1bydKPvAmVYGbd4i1gPDis'
db_file = "pictures.vdb"
endpoint='s3-us-east-2.amazonaws.com'



class States(Enum):
    """
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
    S_START = "0"  # Начало нового диалога
    S_ENTER_NAME = "1"
    S_SEND_PIC = "2"