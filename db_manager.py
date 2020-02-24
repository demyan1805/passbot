import sqlite3
import traceback
import crypt
import telebot

def checkData(action):
    def connectDb(*args):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        res = action(*args, c = c, conn = conn)
        conn.close()
        return res
    return connectDb

@checkData
def addPass(userID, name, login, password, c = None, conn = None):
    try:
        
        cryptedLogin = crypt.encode(str(userID), login)
        cryptedPass = crypt.encode(str(userID), password)
        c.execute('CREATE TABLE IF NOT EXISTS user' + str(userID) + ' (id INTEGER, name TEXT NOT NULL);')
        c.execute('INSERT INTO user' + str(userID) + ' VALUES (?, ?)', (userID, name))
        conn.commit()
        cname=crypt.getHash(name)
        clogin=cryptedLogin[0]
        cpassword=cryptedPass[0]
        lnonce=cryptedLogin[1]
        pnonce=cryptedPass[1]
        c.execute('CREATE TABLE IF NOT EXISTS u' + crypt.getHash(str(userID)) + ' (cname TEXT NOT NULL, clogin TEXT NOT NULL, cpassword TEXT NOT NULL, lnonce TEXT NOT NULL, pnonce TEXT NOT NULL);')
        c.execute('INSERT INTO u' + crypt.getHash(str(userID)) + ' VALUES (?, ?, ?, ?, ?)', (cname, clogin, cpassword, lnonce, pnonce))
        conn.commit()

        res = 'name: <b>' + name + '</b>\n-----\nlogin: <code>' + login + '</code> | password: <code>' + password + '</code>\nWas added!'
    except Exception:
        traceback.print_exc()
        res = 'Something went wrong'
    return res

@checkData
def delPass(userID, name, c = None, conn = None):
    try:
        c.execute('DELETE FROM user' + str(userID) + ' WHERE name = "' + name + '"')
        conn.commit()
        c.execute('DELETE FROM u' + crypt.getHash(str(userID)) + ' WHERE cname = "' + crypt.getHash(name) + '"')
        conn.commit()
        res = name + ' was deleted!'
    except:
        res = 'Ooops!'
    return res

@checkData
def getPass(message, c = None, conn = None):
    name = message.text
    try:
        c.execute('SELECT * FROM user' + str(message.chat.id) + ' WHERE name="' + name + '"')
        res = (c.fetchall() or 'Data not found')
        if (res != 'Data not found'):
            c.execute('SELECT * FROM u' + crypt.getHash(str(message.chat.id)) + ' WHERE cname="' + crypt.getHash(name) + '"')
            raw = c.fetchall()
            res = [name, crypt.decode(str(message.chat.id), raw[0][1], raw[0][3]), crypt.decode(str(message.chat.id), raw[0][2], raw[0][4])]
    except Exception:
        traceback.print_exc()
        res = 'Data not found'
    return res

@checkData
def deleteAll(message, c = None, conn = None):
    try:
        c.execute('DROP TABLE IF EXISTS user' + str(message.chat.id))
        conn.commit()
        c.execute('DROP TABLE IF EXISTS user' + crypt.getHash(str(message.chat.id)))
        conn.commit()
        res = 'All data deleted'
    except:
        res = 'Nothing to delete'
    return res

@checkData
def getNames(message, c = None, conn = None):
    try:
        c.execute('SELECT name FROM user' + str(message.chat.id))
        return c.fetchall()
    except Exception:
        return
