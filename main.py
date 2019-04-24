"""
Telegram Bot to serve NTU students using the Python-Telegram-Bot API.
Created by Pye Sone Kyaw © 2019
"""
import os
from telegram import chat
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import datetime
import pymongo
import calendar

from functions import events
from functions import members
from functions import classes
from functions import dbmanagement
from functions import links
from functions import reminders
from functions import messages

#set up for python-telegram-bot and heroku
TOKEN = "token"
PORT = int(os.environ.get('PORT', '8443'))
NAME = 'name'
updater = Updater(TOKEN)
updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)
updater.start_webhook(listen="0.0.0.0",port=int(PORT),url_path=TOKEN)
updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
dispatcher = updater.dispatcher

#start command to start up bot
def start(bot, update):
	welcome_string = "".join(messages.welcome_text)
	bot.send_message(chat_id=update.message.chat_id, text=welcome_string)
dispatcher.add_handler(CommandHandler('start', start))
job = updater.job_queue

"""
Developer functions
"""
def datetime1(bot,update):
	datetime_object = datetime.datetime.now()
	bot.send_message(chat_id=update.message.chat_id, text=str(datetime_object))

def get_chat_id(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text=("chat_id is " + str(update.message.chat_id)))	

#welcome message. when update sent has new_chat_member, check that the username isnt the bot and if it isnt, send the welcome text string from messages file
def welcome(bot, update):
	for member in update.message.new_chat_members:
		if member.username != 'YourBot':
			welcome_string = "".join(messages.welcome_text)
			bot.send_message(chat_id=update.message.chat_id, text=welcome_string)
#to start timely reminders, theres the daily timetable reminder and weekly reminder. the reminders run off a job queue
def start_reminders(bot,update,job_queue):
	bot.send_message(chat_id=update.message.chat_id, text = 'Starting daily and weekly reminders!')
	job.run_repeating(auto_weekly_events,datetime.timedelta(days=7),datetime.datetime(2019, 3, 15, 21,0,0), context = update.message.chat_id)
	job.run_daily(auto_daily_schedule,datetime.time(hour=22, minute=0, second=0),days=(0,1,2,3,4), context = update.message.chat_id)
#fetches the calendar
def calendar(bot, update):    
	bot.send_document(chat_id=update.message.chat_id, document=links.syllabi["calendar"])
#sends the help text from messages file
def helpme(bot,update):
	help_string="".join(messages.help_text)
	bot.send_message(chat_id=update.message.chat_id, text = help_string)
#auxillary function in case need to shutdown somehow with other options failing
def shutdown():
	updater.stop()
	updater.is_idle = False

#accepts a compliment with thanks
def accept_compliment(bot,update):
        bot.send_message(chat_id=update.message.chat_id, text="😁 Thank you.")

#accepts criticism
def accept_criticism(bot,update):
        bot.send_message(chat_id=update.message.chat_id, text="😞 Sorry I did not live up to your expectations.")

def stop(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="stopping")
	threading.Thread(target=shutdown).start()
#so that random commands won't be met with silence
def unknown(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="😞 Sorry, I didn't understand that command.")
#add functions to dispatcher with what commands to call
dispatcher.add_handler(CommandHandler('syllabus', links.syllabus, pass_args=True))
dispatcher.add_handler(CommandHandler('calendar', calendar))

dispatcher.add_handler(CommandHandler('addmember', members.insert_info, pass_args=True))
dispatcher.add_handler(CommandHandler('getmember', members.get_info, pass_args=True))

dispatcher.add_handler(CommandHandler('addevent', events.add_event, pass_args=True))
dispatcher.add_handler(CommandHandler('getevent', events.get_event, pass_args=True))

dispatcher.add_handler(CommandHandler('addclass', classes.insert_class, pass_args=True))
dispatcher.add_handler(CommandHandler('getclass', classes.get_module, pass_args=True))
dispatcher.add_handler(CommandHandler('getday', classes.get_day, pass_args=True))

dispatcher.add_handler(CommandHandler('delete', dbmanagement.delete, pass_args=True))

dispatcher.add_handler(CommandHandler('tomorrow', reminders.daily_schedule))
dispatcher.add_handler(CommandHandler('week', reminders.weekly_events))
dispatcher.add_handler(CommandHandler('today', reminders.today))
dispatcher.add_handler(CommandHandler('timetable', reminders.timetable1))

dispatcher.add_handler(CommandHandler('reminders', start_reminders, pass_job_queue=True))
dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
dispatcher.add_handler(CommandHandler('help', helpme))

dispatcher.add_handler(CommandHandler('datetime', datetime1))
dispatcher.add_handler(CommandHandler('chatid', get_chat_id))

dispatcher.add_handler(CommandHandler('stop', stop))

dispatcher.add_handler(CommandHandler('goodbot', accept_compliment))
dispatcher.add_handler(CommandHandler('badbot', accept_criticism))

dispatcher.add_handler(MessageHandler(Filters.command, unknown))


updater.idle()

