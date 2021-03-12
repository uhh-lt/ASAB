from telegram.error import ChatMigrated, BadRequest, Unauthorized, TimedOut, NetworkError
from telegram.ext import Updater
from telegram import Poll, Bot, PollOption, User, TelegramError
import os
# import telepot
import random
import csv
import pandas as pd
from flask import Flask, request
from properties.p import Property
from datetime import datetime
from threading import Lock, Thread
from datetime import date
import time

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage

from telegram.utils.request import Request
number_warnning_user = {}
lock = Lock()

user_error_count = {}
user_real = {}
prop = Property()
user_examples = []

max_allowed_tweet = 500  # 500 tweets
max_allowed_time = 600
number_tweet_to_reward = 60 # how many tweets the user should annotate to get crads
controls_per_tweet = 6 # for every 5 tweet, we need one control question

bot_prop = prop.load_property_files('bot.properties')

tweet_id_time = {}
users = []
annotated_tweet_ids = []
annoated_tweet_user_ids = {}
if not os.path.exists('annotated_tweets.csv'):
    columns = ['tweet_id', 'sentiment', 'tweet', 'username']
    columns = ['tweet_id', 'sentiment', 'tweet', 'username']
    df = pd.DataFrame(columns=columns)
    df.to_csv('annotated_tweets.csv', index=False)
else:
    data2 = pd.read_csv('annotated_tweets.csv', encoding='utf8')
    annotated_tweet_ids = data2['tweet_id'].apply(lambda x: int(x)).tolist()
    sentiment = data2['sentiment']
    count = data2['username'].value_counts()
    users = data2['username'].apply(lambda x: str(x)).tolist()

# This is used when we re-annoate the complettd file again.... Since His friend did not finish all
if not os.path.exists('old_annotated_tweets.csv'):
    columns = ['tweet_id', 'sentiment', 'tweet', 'username']
    df = pd.DataFrame(columns=columns)
    df.to_csv('old_annotated_tweets.csv', index=False)
else:
    data2 = pd.read_csv('old_annotated_tweets.csv', encoding='utf8')
    for i in range(len(data2)):
        annoated_tweet_user_ids[data2['tweet_id'][i]] = data2['username'][i]

ans = list()
if not os.path.exists('control_questions.csv'):
    columns = ['tweet', 'class']
    df = pd.DataFrame(columns=columns)
    df.to_csv('control_questions.csv', index=False)
else:
    control_questions = pd.read_csv('control_questions.csv', encoding='utf8')
    for item in zip(control_questions['tweet'], control_questions['class']):
        ans.append((item[0], item[1]))

control = []
if not os.path.exists('control_answers.csv'):
    columns = ['tweet', 'answer', 'username']
    df = pd.DataFrame(columns=columns)
    df.to_csv('control_answers.csv', index=False)
else:
    control_answers = pd.read_csv('control_answers.csv', encoding='utf8')
    for item in zip(control_answers['tweet'], control_answers['answer'], control_answers['username']):
        control.append((item[0], item[1], str(item[2])))

if not os.path.exists('rewarded_cards.txt'):
    f = open('rewarded_cards.txt', 'w', encoding='utf8')
    f.close()

blocked_users = []
if not os.path.exists('blocked_user.txt'):
    f = open('blocked_user.txt', 'w', encoding='utf8')
    f.close()
else:
    blocked_users = [x.strip() for x in open('blocked_user.txt', 'r').readlines()]

if not os.path.exists('log.txt'):
    f = open('log.txt', 'w', encoding='utf8')
    f.close()


data = pd.read_csv('raw_tweets.csv', encoding='utf8', header=0)
raw_tweet_ids = data['tweet_id']

tweet = data['tweet']

user_tweet_ids = {}  # username1 = tweet_id1, username2 = annotated_tweet_ids


tweet_id_to_tweet = dict()
for item in raw_tweet_ids.keys():
    tweet_id_to_tweet[raw_tweet_ids[item]] = tweet[item]

# converting to dict

# display


# bot = telebot.TeleBot(token = TOKEN)
TOKEN = "1081992065:AAE2YjJnyiuZhBFKzWXzkRQgS1DL-I9Tb4U"
Password = bot_prop['PASSWORD']
SEND_EMAIL = bot_prop['SENDEMAIL']
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

text = dict()

keyboard = [[InlineKeyboardButton("ገንቢ", callback_data='Pos'),
             InlineKeyboardButton("አፍራሽ", callback_data='Neg'),
             InlineKeyboardButton("ገለልተኛ", callback_data='Nuet'),
             InlineKeyboardButton("ቅልቅል", callback_data='Mix')]]


def start(update, context):
    # username = update.effective_user.username
    username = str(update.effective_user.id)
    print(update.effective_user.first_name)
    del_timeout_users()


    if username == None:
        update.message.reply_text(
            text="እባክዎን በመጀመሪያ ዩዘርኔም ሴቲንግ ውስጥ ገብተው ይፍጠሩ:: Settings-->click 'username'--> add username here.  ስለ ዩዘርንም አፈጣጠር ለማወቅ ይህንን ቪድዮ ይመልከቱ https://www.youtube.com/watch?v=AOYu40HTQcI&feature=youtu.be")
        return 0

    '''coun = users.count(username)
    if coun == 0:
        update.message.reply_text(
            text="እባክዎን በመጀመሪያ ዩዘርኔም ሴቲንግ ውስጥ ገብተው ይፍጠሩ:: Settings-->click 'username'--> add username here.  ስለ ዩዘርንም አፈጣጠር ለማወቅ ይህንን ቪድዮ ይመልከቱ https://www.youtube.com/watch?v=AOYu40HTQcI&feature=youtu.be")
        return 0'''
    if user_examples.count(username) == 0:
        examples = """ ይህ ሰርቬይ አግባብ ያልሆኑ ቃላት ወይም ንግግሮች ሊኖሩት ይችላል። ዳታውን ያገኘነው ከትዊተር ገፅ ላይ ነው። ከ18 አመት በታች ከሆኑና ተገቢ ያልሆኑ ንግግሮችን ማየት ካልፈለጉ  /end የሚለውን ተጭነው ይውጡ። 
        ምሳሌ \n
        ሰራተኛው አርፋጅ ነው -> አፍራሽ \n
        ልጁ ጥሩ ነው ግን ሰነፈ ነው -> ቅልቅል\n
        ጠንካራ ባህል ያለን ህዝብዎች ነን ->ገምቢ\n
        ቀኑ ሐሙስ ነው  -> ገለልተኛ \n
        ለመቀጠል /start ይጫኑ"""

        update.message.reply_text(text=examples)
        user_examples.append(username)
        return 0

    if username in blocked_users:
        update.message.reply_text(text="እባክዎን በሚቀጥላው ኢሜይል ያግኙን: " + SEND_EMAIL)
        return 0

    coun = users.count(username)  # TODO
    if (int(coun) > max_allowed_tweet):
        update.message.reply_text(text="ሁሉም ዳታ ተሞልቷል እስካሁን የሞሉት ዳታ ተመዝግቦ ተቀምጧል፣ በቀጣይ ዳታ ቅርብ ጊዜ እንለቃለን፣ ተመልሰው ይሞክሩ!!")
        del_timeout_users()
        return 0

    if len(get_five_birs()) + len(get_ten_birs()) == len(get_charged_cards()) or\
            (len(get_five_birs()) % 2 == 1 and
             len(get_five_birs()) + len(get_ten_birs()) - 1 == len(get_charged_cards())):
        update.message.reply_text(text="ትንሽ ቆይተው ይሞክሩ!")
        send_email()
        return 0

    if username in user_tweet_ids and user_tweet_ids[username]:
        update.message.reply_text(text="እባክዎን ከላይ ያለውን መጀመሪያ ይሙሉ!")
        return 0

    reply_markup = InlineKeyboardMarkup(keyboard)

    lock.acquire()

    if (len(annotated_tweet_ids) == len(raw_tweet_ids)):
        message = 'ሁሉም ዳታ ተሞልቷል በቀጣይ ተጨማሪ ሲኖር እናሳውቀዎታለን፤ እናመሰግናለን!!'
        update.message.reply_text(message)
        lock.release()
        return 0

    # if number of tweets are less than the max allowed tweets, we allow only limited users to annotate at a time
    if (len(raw_tweet_ids) - len(annotated_tweet_ids)) / number_tweet_to_reward <= len([v for k,v in user_tweet_ids.items() if v is not None]):
        message = 'እባክዎን ትንሽ ቆይተው /start ብለው ይሞክሩ!!'
        update.message.reply_text(message)
        lock.release()
        return 0

    # if we do not have enough cards
    if len(get_five_birs()) + len(get_ten_birs()) - len(get_charged_cards())  <= len(user_tweet_ids) or \
            (len(get_five_birs()) % 2 == 1 and
             len(get_five_birs()) + len(get_ten_birs()) -1- len(get_charged_cards()) <= len(user_tweet_ids)):
        update.message.reply_text(text="ትንሽ ቆይተው ይሞክሩ!")
        if username in user_tweet_ids:
            del user_tweet_ids[username]
        send_email()
        lock.release()
        return 0

    for x in raw_tweet_ids:
        if x not in annotated_tweet_ids:
            if username in annoated_tweet_user_ids and x in annoated_tweet_user_ids and username == annoated_tweet_user_ids[x]:
                continue;
            if username in user_tweet_ids and user_tweet_ids[username] != None:
                break
            else:
                if x not in [user_tweet_id for user_tweet_id in user_tweet_ids.values()]:
                    user_tweet_ids[username] = x
                    annotated_tweet_ids.append(x)
                    tweet_id_time[username] = time.time()
                    break
    if username in user_tweet_ids:
        update.message.reply_text(tweet_id_to_tweet[user_tweet_ids[username]], reply_markup=reply_markup)
    else:
        update.message.reply_text(text="እናመሰግናለን። አሁን ላይ ሁሉም ዳታ ተሞልቷል። ቀጣይ ዙር ሰርቬይ ሲጀመር እናሳውቀዎታለን!")
    lock.release()


def del_timeout_users():
    expired_users = []
    for uname in tweet_id_time:
        current_time = time.time()
        if current_time - tweet_id_time[uname] >  max_allowed_time:
            expired_users.append(uname)
            if user_tweet_ids[uname] and user_tweet_ids[uname] in annotated_tweet_ids:
                annotated_tweet_ids.remove(user_tweet_ids[uname])
                user_tweet_ids[uname] = None

    for expired_user in expired_users:
        del tweet_id_time[expired_user]


def send_email():
    import smtplib, ssl

    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "tellebott@gmail.com"
    receiver_email = "hizclick@gmail.com"
    password = Password
    message = """no more mobile cards"""

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

def verify(username,fName,uname):
    counter = 0
    message = None
    user_tweet = []
    for item in control:
        if username == item[2]:
            user_tweet.append((item[0], item[1]))

    if len(user_tweet) > 2:  # more than two mistakes
        for x in range(max(len(user_tweet) - 4, 0), len(user_tweet)):
            if user_tweet[x] in ans:
                counter = 0
                continue
            else:
                counter = counter + 1
            if counter == 3:
                message = "warning"
                number_warnning_user[username] = number_warnning_user.get(username,0) +1
            elif counter > 3:
                message = "block"

    if counter >= 4 or number_warnning_user.get(username,0)>2:
        message = "block"
        with open('blocked_user.txt', 'a', encoding='utf8') as f:
            if uname is None:
                uname = 'no username'
            if fName is None:
                fName = 'No first name'
            blocked_users.append(username)
            f.write(username+ ' ' + uname + ' ' + fName +  "\n")
    print ("verify message = ", message)
    return message

def get_charged_cards():
    fil = open('rewarded_cards.txt', 'r', encoding='utf8')
    rewarded_cards = fil.readlines()
    re = []
    for x in rewarded_cards:
        j = x.replace(' ', '')
        re.append(j.rstrip('\n').split('\t')[0])
    while ('' in re):
        re.remove('')
    return re

def get_ten_birs():
    f2 = open('10birr.txt', 'r', encoding='utf8')
    ten = f2.readlines()
    te = []
    for x in ten:
        j = x.strip()
        te.append(j.rstrip('\n'))
    while ('' in te):
        te.remove('')

    return te


def get_five_birs():
    f = open('5birr.txt', 'r', encoding='utf8')
    five = f.readlines()
    fiv = []
    for x in five:
        j = x.strip()
        fiv.append(j.rstrip('\n'))
    while ('' in fiv):
        fiv.remove('')

    return fiv


def prise(num, username):

    lock.acquire()
    message = "እንኳ ደስ አለዎት የ" + str(num) + " ብር ካርድ አሸናፊ ሆነዋል። የካርድ ቁጥርዎ የሚከተሉት ናቸው፦ "
    fiv = get_five_birs()
    re = get_charged_cards()
    te = get_ten_birs()

    user_cards = []
    user_cards.extend(re)
    number = ''
    cnt = 0

    for n in te:
        if str(n) not in user_cards:
            user_cards.append(n)
            number = number + ' ካርድ ቁጥር :- ' + str(n)
            fil = open('rewarded_cards.txt', 'a', encoding='utf8')
            fil.writelines(str(n) + '\t' + '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.now()) + '\t' + username + "\n")
            fil.close()
            break

    for n in fiv:
        if str(n) not in user_cards:
            user_cards.append(n)
            number = number + ' ካርድ ቁጥር :- ' + str(n)
            fil = open('rewarded_cards.txt', 'a', encoding='utf8')
            fil.writelines(str(n) + '\t' + '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.now()) + '\t' + username + "\n")
            fil.close()
            cnt += 1
            if cnt > 1:
                break
    lock.release()
    return message + number



def button(update, context):
    username = str(update.effective_user.id)
    uname = str(update.effective_user.username)
    fName  = str(update.effective_user.first_name)
    del_timeout_users()
    query = update.callback_query
    if len(get_five_birs()) + len(get_ten_birs()) <= len(get_charged_cards()):
        query.edit_message_text(text="ትንሽ ቆይተው ይሞክሩ!")
        print("+++++++++ADMINS, Please add cards to continue the annotation.+++++")
        send_email()
        return 0

    if username == None:
        query.edit_message_text(
            text="እባክዎን በመጀመሪያ ዩዘርኔም ሴቲንግ ውስጥ ገብተው ይፍጠሩ::Settings-->Edit Profile-->Add username--Save. ለበለጠ መረጃ https://www.youtube.com/watch?v=AOYu40HTQcI&feature=youtu.be")
        return 0

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
   # query.answer()

    coun = users.count(username)  # TODO
    print("count for username ",username, "is", coun)
    if uname is None:
        uname = 'no username'
    if fName is None:
        fName = 'No first name'
    with open('log.txt', 'a', encoding='utf8') as f:
        f.write(username + " " + uname + " " + fName + "\n")
    val = coun % controls_per_tweet
    if (int(coun) > max_allowed_tweet):
        query.edit_message_text(text="ሁሉም ዳታ ተሞልቷል እስካሁን የሞሉት ዳታ ተመዝግቦ ተቀምጧል፣ በቀጣይ ዳታ ቅርብ ጊዜ እንለቃለን፣ ተመልሰው ይሞክሩ!!")
        del_timeout_users()
        return 0

    if coun % number_tweet_to_reward == 0 and coun != 0:
        pr = prise(10,username) + " ለመቀጠል /start ይጫኑ!"
        if username in user_tweet_ids and  user_tweet_ids[username]:
            write(query, username)
        elif username in user_real:
            write_correct(query, username, user_real[username])
        query.edit_message_text(text=pr)
        print(username +' ' + pr)
        return 0

    if username in user_tweet_ids and user_tweet_ids[username] is not None:
        write(query, username)
    elif username in user_real and user_real[username]:
        write_correct(query,username,user_real[username])
        message = verify(username,fName,uname)
        if message == 'warning':
            query.edit_message_text(text="ተደጋጋሚ ስህተት እየሰሩ ነው፤ እባክዎን ተጠንቅቀው ይሙሉ, ለመቀጠል /start ይጫኑ!")
            user_tweet_ids[username] = None
            return 0
        elif message == 'block':
            query.edit_message_text(text="ተደጋጋሚ ስህተት ስለ ሰሩ አካውንቶ ታግዶአል፡፡")
            return 0

    if (len(annotated_tweet_ids) == len(raw_tweet_ids)):
        message = 'ሁሉም ዳታ ተሞልቷል እስካሁን የሞሉት ዳታ ተመዝግቦ ተቀምጧል፣ በቀጣይ ዳታ በቅርብ ጊዜ እንለቃለን፣ ተመልሰው ይሞክሩ!!'
        query.edit_message_text(text=message)
        return 0

    if val == 0:
        reply_markup = InlineKeyboardMarkup(keyboard)
        user_real[username]  = real_control()
        query.edit_message_text(text=user_real[username])
        query.edit_message_reply_markup(reply_markup=reply_markup)
    else:
        for x in raw_tweet_ids:
            if x not in annotated_tweet_ids:
                if username in annoated_tweet_user_ids and username == annoated_tweet_user_ids[x]:
                    continue;
                if username in user_tweet_ids and  user_tweet_ids[username]:
                    break
                elif x not in [user_tweet_id for user_tweet_id in user_tweet_ids.values()]:
                    user_tweet_ids[username] = x
                    annotated_tweet_ids.append(x)
                    tweet_id_time[username] = time.time()
                    eval(query, x, tweet_id_to_tweet[user_tweet_ids[username]], username)
                    break



def write_correct(query, username, message):
    with open('control_answers.csv', 'a', encoding='utf8') as f:
        lock.acquire()
        try:
            writer = csv.writer(f)
            writer.writerow([message, format(query.data), str(username)])
            control.append((message, format(query.data), str(username)))
            user_real[username] = None
            users.append(username)
        except:
            print("error in control")
        lock.release()


def eval(query, tweet_id, tweet, username):
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=tweet)
    query.edit_message_reply_markup(reply_markup=reply_markup)


def real_control():
    import random
    tweet = list()
    for item in ans:
        tweet.append(item[0])
    return random.choice(tweet)


def write(query, username):
    with open('annotated_tweets.csv', 'a', encoding='utf8') as f:

        lock.acquire()
        try:
            writer = csv.writer(f)
            writer.writerow([user_tweet_ids[username], format(query.data), tweet_id_to_tweet[user_tweet_ids[username]], str(username)])
            print([user_tweet_ids[username], format(query.data), tweet_id_to_tweet[user_tweet_ids[username]], str(username)])
            user_tweet_ids[username] = None
            users.append(username)
        except:
            print("error is here")
            print("error is here", username)
            print("error is here", user_tweet_ids[username])
            print("error is here", tweet_id_to_tweet)

        lock.release()


def help(update, context):
    update.message.reply_text("Use /start to test this bot.")


def end(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='ስለ ትብብርዎ እናመሰግናለን!')


def error(update, context):
    try:
        raise error
    except Unauthorized:
        logging.debug("TELEGRAM ERROR: Unauthorized - %s" % error)
    except BadRequest:
        logging.debug("TELEGRAM ERROR: Bad Request - %s" % error)
    except TimedOut:
        logging.debug("TELEGRAM ERROR: Slow connection problem - %s" % error)
        message = 'Timeout, /start የሚለውንንይሞክሩ!'
        query = update.callback_query
        update.message.reply_text(text=message)
    except NetworkError:
        logging.debug("TELEGRAM ERROR: Other connection problems - %s" % error)
    except ChatMigrated as e:
        logging.debug("TELEGRAM ERROR: Chat ID migrated?! - %s" % error)
    except TelegramError:
        logging.debug("TELEGRAM ERROR: Other error - %s" % error)
    except:
        try:
            import traceback

            print(traceback.format_exc())

            logging.debug("TELEGRAM ERROR: Unknown - %s" % error)
            """Log Errors caused by Updates."""
            logger.warning('Update "%s" caused error "%s"', update, context.error)
            message = 'እባክዎ እንደገና ይሞክሩ, /start የሚለውን ንይሞክሩ!'
            print(message)
            query = update.callback_query
            print(message,"Again")
            query.edit_message_text(text=message)
        except:
            print('Worst error! No idea')

    return 0


def instruction(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='ጽሁፉ ገምቢ ከሆነ "ገምቢ" የሚለውን፣ አፍራሽ ከሆነ "አፍራሽ" የሚለውን፣ ገለልትኛ "ገለልተኛ" የሚለውን ፣ የገምቢ እና የአፍራሽ ቅልቅል ከሆነ "ቅልቅል" የሚለውን ይምረጡ፡፡ ይህንን መረጃ ሲሞሉ በትክክል በመለሱት ጥያቄ ልክ በዕለቱ መጨረሻ በእርስዎ "user name" በኩል የሞባይል ካርድ ሽልማት ይላክለዎታል። ለበለጠ መረጃ https://annotation-wq.github.io/')


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('end', end))
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('instruction', instruction))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()

