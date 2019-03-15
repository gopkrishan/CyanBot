import pymongo
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
client = pymongo.MongoClient("")
db = client[""]
members = db[""]
events = db[""]
timetable = db[""]

def delete(bot,update,args):
	if (len(args)<=1):
		bot.send_message(chat_id=update.message.chat_id, text="Please enter whether it's a member, event or class to delete")
		return
	else:
		nature = args[0]
		if (nature == "member"):
			deletee = ""
			for x in args[1:]:
				deletee += x
			query = { "name": deletee}
			members.delete_one(query)
			bot.send_message(chat_id=update.message.chat_id, text="Deleted " + deletee.title() + " from members database")
		if (nature == "event"):
			deletee = ""
			for x in args[1:]:
				deletee += x
			query = { "name": deletee}
			events.delete_one(query)
			bot.send_message(chat_id=update.message.chat_id, text="Deleted " + deletee.title() + " from events database")
		if (nature == "class"):
			fields = ["nature:", "code:"]
			_in=args[1:]
			_dict = {}
			for i in range(len(_in)):
				if _in[i].lower() in fields:
					found_field_index = i
					j=i+1
					while j<len(_in) and (_in[j].lower() not in fields) :
						j+=1
					found_field_value = ""
					for k in range(i+1,j):
						found_field_value+=(_in[k].lower() + " ")
						_dict[(_in[i].lower())[:-1]]=found_field_value
			print(_dict)
			nature = _dict["nature"].rstrip()
			code = _dict["code"].rstrip()
			query = {"code":code.upper(), "nature":nature}
			timetable.delete_one(query)
			bot.send_message(chat_id=update.message.chat_id, text="Deleted " + code.upper() + " " + nature.title() + " from timetable")