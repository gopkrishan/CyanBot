from telegram import chat
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters, CommandHandler
import datetime

import pymongo
import datetime 
import calendar
client = pymongo.MongoClient("")
db = client[""]
members = db[""]
events = db[""]
timetable = db[""]

def daily_schedule(bot,update):
	tomorrow_day = (datetime.datetime.today()+ datetime.timedelta(days=1)).strftime('%A')
	tomorrow_date = str((datetime.datetime.today()+ datetime.timedelta(days=1)).date())
	daily = ""
	daily += "📝 Here's your nightly reminder for tomorrow!\n"
	daily += "====================\n"
	daily += (tomorrow_day + "'s timetable!\n")
	if (tomorrow_day == "Saturday" or tomorrow_day == "Sunday"):
		bot.send_message(chat_id=update.message.chat_id, text="It's a weekend tomorrow!")
		return
	query ={"day": tomorrow_day.lower()}
	for x in timetable.find(query,{ "_id": 0,"name": 1, "nature": 1, "start":1, "end":1, "location":1, "code":1}).sort("start"):
		daily += ("====================\n")
		daily += ("📌 " + x["name"].upper() + "\n")
		daily += ("Type: " + x["nature"].title() + "\n")
		daily += ("⏳ " + x["start"] + "\n")
		daily += ("⌛ " + x["end"] + "\n")
		daily += ("📍 " + x["location"].upper() + "\n")
	query = {"date": tomorrow_date}
	for y in events.find(query,{ "_id": 0,"name": 1, "start":1, "end":1, "location":1}).sort("start"):
		daily += ("====================\n")
		daily += ("📎 " + y["name"].upper() + "\n")
		daily += ("⏳ " + y["start"] + "\n")
		daily += ("⌛ " + y["end"] + "\n")
		daily += ("📍 " + y["location"].upper() + "\n")
	bot.send_message(chat_id=update.message.chat_id, text=daily)

def today(bot,update):
	today_day = (datetime.datetime.today()).strftime('%A')
	today_date = str((datetime.datetime.today()).date())
	if (today_day == "Saturday" or today_day == "Sunday"):
		bot.send_message(chat_id=update.message.chat_id, text="It's a weekend today!")
		return
	daily = ""
	daily += "📝 Here's your schedule for today!\n"
	daily += "====================\n"
	daily += (today_day + "'s timetable!\n")

	query ={"day": today_day.lower()}

	for x in timetable.find(query,{ "_id": 0,"name": 1, "nature": 1, "start":1, "end":1, "location":1, "code":1}).sort("start"):

		daily += ("====================\n")
		daily += ("📌 " + x["name"].upper() + "\n")
		daily += ("Type: " + x["nature"].title() + "\n")
			
		daily += ("⏳ " + x["start"] + "\n")
		daily += ("⌛ " + x["end"] + "\n")
		daily += ("📍 " + x["location"].upper() + "\n")

	query = {"date": today_date}
	for y in events.find(query,{ "_id": 0,"name": 1, "start":1, "end":1, "location":1}).sort("start"):
		daily += ("====================\n")
		daily += ("📎 " + y["name"].upper() + "\n")
		daily += ("⏳ " + y["start"] + "\n")
		daily += ("⌛ " + y["end"] + "\n")
		daily += ("📍 " + y["location"].upper() + "\n")
	bot.send_message(chat_id=update.message.chat_id, text=daily)

def auto_daily_schedule(bot,job):
	tomorrow_day = (datetime.datetime.today()+ datetime.timedelta(days=1)).strftime('%A')
	tomorrow_date = str((datetime.datetime.today()+ datetime.timedelta(days=1)).date())
	if (tomorrow_day == "Saturday" or tomorrow_day == "Sunday"):
		return
	daily = ""
	daily += "📝 Here's your nightly reminder for tomorrow!\n"
	daily += "====================\n"
	daily += (tomorrow_day + "'s timetable!\n")
	
	query ={"day": tomorrow_day.lower()}

	for x in timetable.find(query,{ "_id": 0,"name": 1, "nature": 1, "start":1, "end":1, "location":1, "code":1}).sort("start"):
			
		daily += ("====================\n")
		daily += ("📌 " + x["name"].upper() + "\n")
		daily += ("Type: " + x["nature"].title() + "\n")
			
		daily += ("⏳ " + x["start"] + "\n")
		daily += ("⌛ " + x["end"] + "\n")
		daily += ("📍 " + x["location"].upper() + "\n")
	query = {"date": tomorrow_date}
	for y in events.find(query,{ "_id": 0,"name": 1, "start":1, "end":1, "location":1}).sort("start"):
		print(y)
		daily += ("====================\n")
		daily += ("📎 " + y["name"].upper() + "\n")
		daily += ("⏳ " + y["start"] + "\n")
		daily += ("⌛ " + y["end"] + "\n")
		daily += ("📍 " + y["location"].upper() + "\n")
	bot.send_message(chat_id=job.context, text=daily)


def weekly_events(bot,update):
	dates_of_week=[
			str((datetime.datetime.today()).date()),
			str((datetime.datetime.today()+ datetime.timedelta(days=1)).date()),
			str((datetime.datetime.today()+ datetime.timedelta(days=2)).date()),
			str((datetime.datetime.today()+ datetime.timedelta(days=3)).date()),
			str((datetime.datetime.today()+ datetime.timedelta(days=4)).date()),
			str((datetime.datetime.today()+ datetime.timedelta(days=5)).date()),
			str((datetime.datetime.today()+ datetime.timedelta(days=6)).date()),
			str((datetime.datetime.today()+ datetime.timedelta(days=7)).date()),
		]
	daily = ""
	daily += "📝 Here's your weekly reminder!\n"
	
	for x in events.find({},{ "_id": 0,"name": 1, "start":1, "end":1, "location":1, "date":1}).sort([("date", 1), ("start", 1)]):
		if x["date"] in dates_of_week:
			daily += ("====================\n")
			daily += ("📎 " + x["name"].title() + "\n")
			daily += ("🗓 " + format_db_date(x['date']) + "\n")
				
			daily += ("⏳ " + x["start"] + "\n")
			daily += ("⌛ " + x["end"] + "\n")
			daily += ("📍 " + x["location"].upper() + "\n")
	bot.send_message(chat_id=update.message.chat_id, text=daily)

def timetable1(bot,update):
	dates_of_week=[
			str((datetime.datetime.today()).date()),
			str((datetime.datetime.today()+ datetime.timedelta(days=1)).date()),
			str((datetime.datetime.today()+ datetime.timedelta(days=2)).date()),
			str((datetime.datetime.today()+ datetime.timedelta(days=3)).date()),
			str((datetime.datetime.today()+ datetime.timedelta(days=4)).date()),
			str((datetime.datetime.today()+ datetime.timedelta(days=5)).date()),
			str((datetime.datetime.today()+ datetime.timedelta(days=6)).date()),
			str((datetime.datetime.today()+ datetime.timedelta(days=7)).date()),
		]
	days_of_week=['monday','tuesday','wednesday','thursday','friday']
	weekly = ""
	weekly += "📝 Here's your weekly timetable!\n"
	weekly += ("====================\n")
	for x in days_of_week:
		
		day_classes = timetable.find({"day": x},{ "_id": 0,"name": 1, "nature":1, "code":1, "start":1, "end":1, "location":1, "day":1}).sort([("day", 1), ("start", 1)])
		weekly += ("🗓 " + x.title() + "\n")
		for y in day_classes:
			
			weekly += ("---------------------\n")
			weekly += ("📌 " + y["name"].upper() + "\n")
			weekly += ("Type: " + y["nature"].title() + "\n")
			
			weekly += ("⏳ " + y["start"] + "\n")
			weekly += ("⌛ " + y["end"] + "\n")
			weekly += ("📍 " + y["location"].upper() + "\n")
		weekly += ("====================\n")
	
	bot.send_message(chat_id=update.message.chat_id, text=weekly)



def auto_weekly_events(bot,job):
	dates_of_week=[
			str((datetime.datetime.today()).date()),
			str((datetime.datetime.today()+ datetime.timedelta(days=1)).date()),
			str((datetime.datetime.today()+ datetime.timedelta(days=2)).date()),
			str((datetime.datetime.today()+ datetime.timedelta(days=3)).date()),
			str((datetime.datetime.today()+ datetime.timedelta(days=4)).date()),
			str((datetime.datetime.today()+ datetime.timedelta(days=5)).date()),
			str((datetime.datetime.today()+ datetime.timedelta(days=6)).date()),
			str((datetime.datetime.today()+ datetime.timedelta(days=7)).date()),
		]
	daily = ""
	daily += "📝 Here's your weekly reminder!\n"
	
	for x in events.find({},{ "_id": 0,"name": 1, "start":1, "end":1, "location":1, "date":1}).sort([("date", 1), ("start", 1)]):
		if x["date"] in dates_of_week:
			daily += ("====================\n")
			daily += ("📎 " + x["name"].title() + "\n")
			daily += ("🗓 " + format_db_date(x['date']) + "\n")
				
			daily += ("⏳ " + x["start"] + "\n")
			daily += ("⌛ " + x["end"] + "\n")
			daily += ("📍 " + x["location"].upper() + "\n")
	bot.send_message(chat_id=job.context, text=daily)




