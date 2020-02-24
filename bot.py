import config
import crypt
import answers
import keyboard
import db_manager
from state_manager import *
import actions
import telebot
from aiohttp import web
import ssl
import time


bot = telebot.TeleBot(config.token)
app = web.Application()

async def handle(request):
    request_body_dict = await request.json()
    update = telebot.types.Update.de_json(request_body_dict)
    bot.process_new_updates([update])
    return web.Response()

app.router.add_post('/' + config.token + '/', handle)

@bot.message_handler(commands=['start'])
def start_message(message):
    activeMessage = bot.send_message(message.chat.id, 'Hello!\n' + answers.HELP_MESSAGE, reply_markup=keyboard.getDefault(), parse_mode='HTML')
    setState(str(message.chat.id), createAction(actions.setActiveMessage, activeMessage))
    setState(str(message.chat.id), createAction(actions.done))
    deleteMessage(message)

@bot.message_handler(commands=['help'])
def help_message(message):
    activeMessage = bot.send_message(message.chat.id, answers.HELP_MESSAGE, reply_markup=keyboard.getDefault(), parse_mode='HTML')
    setState(str(message.chat.id), createAction(actions.setActiveMessage, activeMessage))
    setState(str(message.chat.id), createAction(actions.done))
    deleteMessage(message)

@bot.message_handler(content_types=['text'])
def answer(message):
    currentState = getState(str(message.chat.id))
    sendAnswer(message, currentState)

def sendAnswer(message, state):
    activeMessage = state.get('ACTIVE_MESSAGE')
    res = 'Ooops!'
    keyboardMarkup = keyboard.getDefault()
    if activeMessage!=None:
        if (message.date - activeMessage.date < 151200):
            bot.delete_message(message.chat.id, activeMessage.message_id)
        activeMessage = None

    if message.text == keyboard.cancelBtn or message.text == keyboard.backBtn:
        setState(str(message.chat.id), createAction(actions.done))
        res = answers.MAINMENU

    elif state.get('DONE'):

        if message.text[:4].lower() == 'add ':
            messageData = message.text.split()
            name = messageData[1]
            login = messageData[2]
            password = messageData[3]
            res = db_manager.addPass(message.chat.id, name, login, password)
            
        elif message.text[:4].lower() == 'del ':
            messageData = message.text.split()
            name = messageData[1]
            res = db_manager.delPass(message.chat.id, name)

        elif message.text == 'DELETE ALL':
            res = db_manager.deleteAll(message)

        elif message.text == keyboard.addBtn:
            setState(str(message.chat.id), createAction(actions.add))
            res = answers.ADDNAME
            keyboardMarkup = keyboard.getCancel()

        elif message.text == keyboard.delBtn:
            setState(str(message.chat.id), createAction(actions.delete))
            res = answers.DELNAME
            keyboardMarkup = keyboard.getList(db_manager.getNames(message))

        elif message.text == keyboard.listBtn:
            res = answers.LISTTITLE
            keyboardMarkup = keyboard.getList(db_manager.getNames(message))

        else:
            res = db_manager.getPass(message)
            if res != 'Data not found':
                deleteMessage(message)
                activeMessage = bot.send_message(message.chat.id, '<b>' + res[0] + '</b>\nlogin: <code>' + res[1] + '</code>\npassword: <code>' + res[2] + '</code>', reply_markup=keyboardMarkup, parse_mode='HTML')
                setState(str(message.chat.id), createAction(actions.setActiveMessage, activeMessage))
                return
                
    elif state.get('ADD'):
        if state['LOGIN']:
            state = setState(str(message.chat.id), createAction(actions.addPass, message.text))
            res = db_manager.addPass(message.chat.id, state['NAME'], state['LOGIN'], state['PASS'])
            state = None
            setState(str(message.chat.id), createAction(actions.done))
        elif state['NAME']:
            state = setState(str(message.chat.id), createAction(actions.addLogin, message.text))
            res = answers.ADDPASS
            keyboardMarkup = keyboard.getCancel()
        else:
            state = setState(str(message.chat.id), createAction(actions.addName, message.text))
            res = answers.ADDLOGIN
            keyboardMarkup = keyboard.getCancel()

    elif state.get('DEL'):
        if state['NAME']:
            if message.text == keyboard.accept:
                state = setState(str(message.chat.id), createAction(actions.confirm, message.text))
                res = db_manager.delPass(message.chat.id, state['NAME'])
            else:
                res = 'Действие отменено'
            state = None
            setState(str(message.chat.id), createAction(actions.done))
        else:
            state = setState(str(message.chat.id), createAction(actions.deleteName, message.text))
            res = answers.CONFIRMATION + message.text + '?'
            keyboardMarkup = keyboard.getConfirmation()

    deleteMessage(message)
    activeMessage = bot.send_message(message.chat.id, res, reply_markup=keyboardMarkup, parse_mode='HTML')
    setState(str(message.chat.id), createAction(actions.setActiveMessage, activeMessage))


def deleteMessage(message):
    bot.delete_message(message.chat.id, message.message_id)

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain(config.SSL_CERT, config.SSL_KEY)

# start aiohttp server (our bot)
web.run_app(
    app,
    host=config.HOOK_IP,
    port=config.HOOK_PORT,
    ssl_context=context,
)