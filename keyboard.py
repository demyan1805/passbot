import telebot

addBtn = 'Добавить пароль'
delBtn = 'Удалить пароль'
listBtn = 'Сохраненные пароли'
cancelBtn = 'Отмена'
backBtn = 'Назад'
accept = 'Да'
decline = 'Нет'

defaultKeyboard = telebot.types.ReplyKeyboardMarkup(False, True)
listButton = telebot.types.KeyboardButton(listBtn)
addButton = telebot.types.KeyboardButton(addBtn)
delButton = telebot.types.KeyboardButton(delBtn)
defaultKeyboard.row(listButton)
defaultKeyboard.row(addButton, delButton)

def getDefault():
    return defaultKeyboard

def getConfirmation():
    keyboard = telebot.types.ReplyKeyboardMarkup(False, True)
    confirmBtn = telebot.types.KeyboardButton(accept)
    declineBtn = telebot.types.KeyboardButton(decline)
    keyboard.row(confirmBtn, declineBtn)
    return keyboard

def getCancel():
    keyboard = telebot.types.ReplyKeyboardMarkup(False, True)
    cancel = telebot.types.KeyboardButton(cancelBtn)
    keyboard.row(cancel)
    return keyboard

def getList(names, sort=True):
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True, row_width=1)
    keyboard.add(telebot.types.KeyboardButton(backBtn))
    if sort:
        names.sort()
    if (len(names) > 0):
        for name in names:
            keyboard.add(telebot.types.KeyboardButton(name[0]))
    else:
        keyboard = telebot.types.ReplyKeyboardRemove()
    return keyboard