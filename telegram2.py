import telebot
import sqlite3
from sqlite3 import Error
import random, time
#import mnogochlen
#import weather2fromweathermap
bot = telebot.TeleBot('1836713851:AAHnJhLnZX-aFlDlh5om8a1iPLIvXtbFxHI')
#======================================================
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection
connection = create_connection("telegram1bot.sqlite")
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
create_users_table = """
CREATE TABLE IF NOT EXISTS users(
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  rights TEXT
  );
"""
execute_query(connection, create_users_table)
def execute_read_query(connection, query):

    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

        
#==========================sqlite ended=========
def isadmin(userid):
    connection = create_connection("telegram1bot.sqlite")
    select_users = "SELECT * from users where id="+str(userid)+";"
    users = execute_read_query(connection, select_users)
    allusers=''
    for user in users:
        allusers+=str(user)
    if (allusers).count(str(userid))>0:
        return True
    else:
        return False
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f'Я бот. Приятно познакомиться, {message.from_user.first_name}')
    bot.send_message(message.from_user.id, 'используй /help чтобы узнать все возможности')
    print(message.from_user.id)
    newuser='insert into users values('+str(message.from_user.id)+',"'+message.from_user.first_name+'","user");'
    connection = create_connection("telegram1bot.sqlite")

    execute_query(connection, newuser)
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, 'команды: /start, /help, /mathhelp')
    bot.reply_to(message, 'запросы: привет, помоги с математикой, рандом, рандомное число от m до n, погода')
@bot.message_handler(commands=['mathhelp'])
def send_mathhelp(message):
    bot.reply_to(message, 'используй слово матеша в начале сообщения')
@bot.message_handler(commands=['mnogochlen'])
def mnogochlen(message):
    bot.reply_to(message, 'hello, my king')
    upgradeuser='UPDATE users set rights="admin" where id="'+str(message.from_user.id)+'";'
    connection = create_connection("telegram1bot.sqlite")
@bot.message_handler(commands=['showallusers'])
def showallusers(message):
    if isadmin(message.from_user.id)==True:
        connection = create_connection("telegram1bot.sqlite")
        select_users = "SELECT * from users;"
        users = execute_read_query(connection, select_users)
        allusers=''
        for user in users:
            allusers+=str(user)
        bot.send_message(message.from_user.id,allusers)
@bot.message_handler(commands=['makerepository'])
def makerepository(message):
    if isadmin(message.from_user.id)==True:
        connection = create_connection("telegram1bot.sqlite")
        create_repository = "CREATE TABLE IF NOT EXISTS userrepository"+str(message.from_user.id)+"(number INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,content TEXT not null);"
        execute_query(connection, create_repository)
        bot.send_message(message.from_user.id,'good')
@bot.message_handler(commands=['writeinrepository'])
def writeinrepository(message):
    if isadmin(message.from_user.id)==True:
        try:
            thismessage=((message.text).replace('/writeinrepository ','')).split('|')
        

            connection = create_connection("telegram1bot.sqlite")
            write_in_repository = "insert into userrepository"+str(message.from_user.id)+"(name, content) values('"+thismessage[0]+"', '"+thismessage[1]+"');"
            print(write_in_repository)
            execute_query(connection, write_in_repository)
            bot.send_message(message.from_user.id,'good')
        except Exception as e:
            bot.send_message(message.from_user.id,str(e))
@bot.message_handler(commands=['deletefromrepository'])
def deletefromrepository(message):
    if isadmin(message.from_user.id)==True:
        try:
            thismessage=((message.text).replace('/deletefromrepository ',''))
        

            connection = create_connection("telegram1bot.sqlite")
            write_in_repository = "delete from userrepository"+str(message.from_user.id)+" where name='"+thismessage+"';"
            print(write_in_repository)
            execute_query(connection, write_in_repository)
            bot.send_message(message.from_user.id,'good')
        except Exception as e:
            bot.send_message(message.from_user.id,str(e))            
@bot.message_handler(commands=['showrepository'])
def showrepository(message):
    if isadmin(message.from_user.id)==True:
        connection = create_connection("telegram1bot.sqlite")
        show_repository = "select * from userrepository"+str(message.from_user.id)+";"
        repository=execute_read_query(connection, show_repository)
        bot.send_message(message.from_user.id,str(repository)+'v')

@bot.message_handler(content_types=['audio'])
def send_the_fuck(message):
    bot.send_message(message.from_user.id,'шо за хуйня')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'привет': 
        bot.send_message(message.from_user.id, 'Привет!')
    """elif message.text.lower() in ('погода', 'погода в екатеринбурге', 'weather', 'weather in ekaterinburg'):
        bot.send_message(message.from_user.id, weather2fromweathermap.weathernow('Ekaterinburg,RU'))
    elif message.text.lower() in ('погода завтра', 'погода на завтра', 'погода на 5 дней', 'погода в екатеринбурге на завтра', 'weather tomorrow', 'weather in ekaterinburg tomorrow'):
        bot.send_message(message.from_user.id, weather2fromweathermap.weathertomorrow('Ekaterinburg,RU'))"""
    elif message.text.lower().count('матеша')>0:
        try:
            bot.send_message(message.from_user.id, mnogochlen.mix((message.text.lower()).replace('матеша', '')))
        except Exception as e:
            bot.send_message(message.from_user.id, str(e))
            
    elif message.text.lower() == 'помоги с математикой':
        bot.send_message(message.from_user.id, 'без проблем, что ты хочешь, узнай больше с помощью /mathhelp')
    elif message.text.lower() in ('рандом', 'сгенерируй рандомное число от 0 до 1'):
        bot.send_message(message.from_user.id, random.random())
    elif ((message.text.lower()).count('рандомное число')>0 or (message.text.lower()).count('рандомная цифра')>0) and ((message.text.lower()).count('от')>0 and (message.text.lower()).count('до')>0):
        thismessage=(message.text.lower()).split(' ')
        minint=''
        maxint=''
        
        for i in range (len(thismessage)):
            if thismessage[i].isdigit():
                if minint=='':
                    minint=int(thismessage[i])
                else :
                    maxint=int(thismessage[i])
        if minint>maxint:
            minint,maxint=int(maxint),int(minint)
            
        bot.send_message(message.from_user.id, random.randint(minint, maxint))
    else:
        bot.send_message(message.from_user.id, 'Не понимаю, что это значит.')
bot.polling(none_stop=True)
#'сгенерируй рандомную цифру'
