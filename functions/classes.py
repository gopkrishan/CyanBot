import pymongo
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
client = pymongo.MongoClient("")
db = client[""]
timetable = db[""]

def insert_class(bot,update,args):
	fields = ['name:', "nature:", "start:", "end:","location:", "day:","code:"]
	fields_1 = ['name', "nature", "start", "end","location", "day","code"]
	_in=args
	#check whether the args list has the strings or not. if they do, whatever is after the field will be the value of the key(field) in the dict
	_dict = {'name':'Nil','nature':'Nil','start':'Nil','end':'Nil','location':"Nil",'day':'Nil',"code":"Nil"}
	for i in range(len(_in)):
		if (_in[i].lower() in fields) or (_in[i].lower() in fields_1):
			found_field_index = i
			j=i+1
			while j<len(_in) and (_in[j].lower() not in fields) and (_in[j].lower() not in fields_1):
				j+=1
			found_field_value = ""
			for k in range(i+1,j):
				found_field_value+=(_in[k].lower() + " ")
				if (_in[i].lower() in fields):
					_dict[(_in[i].lower())[:-1]]=found_field_value
				elif (_in[i].lower() in fields_1):
					_dict[(_in[i].lower())]=found_field_value
	#remove whitespace from the previous permutation
	name = _dict["name"].rstrip().upper()
	nature = _dict["nature"].rstrip()
	day  = _dict["day"].rstrip()
	start = _dict["start"].rstrip()
	end = _dict["end"].rstrip()
	location = _dict["location"].rstrip()
	code = _dict["code"].rstrip()
	#enter to database
	if (timetable.count_documents({"name":name, "nature":nature, "day":day}) == 0):
		bot.send_message(chat_id=update.message.chat_id, text="👶 Adding new class: "+name.upper())
		class_entry = { "name": name.lower(), "nature": nature, "day": day.lower(), "start": start, "end": end, "location": location.lower(), "code": code.lower() }
		timetable.insert_one(class_entry)
	else:
		bot.send_message(chat_id=update.message.chat_id, text="🧒 Editing existing class: "+name.upper())
		query = {"name":name.upper(), "nature":nature, "day":day}
		update = { "$set": { "nature": nature, "day": day.lower(), "start": start, "end": end, "location": location.lower() } }
		timetable.update_one(query, update)


def get_module(bot,update,args):
	if (len(args)==0):
		bot.send_message(chat_id=update.message.chat_id, text="🧒 🧒 Please enter /getclass followed by the module's code")
		return
	code = args[0]
	if (timetable.count_documents({"code": code.lower()})==0):
		bot.send_message(chat_id=update.message.chat_id, text="😞 Module does not exist in database, please try again")
	else:
		bot.send_message(chat_id=update.message.chat_id, text="🧒 Getting information for: " + code.upper())
		query ={"code": code.lower()}
		reply = ""
		reply += ("🏫 " + code.upper() + "\n")
		for x in timetable.find(query,{ "_id": 0,"name": 1, "nature": 1, "start":1, "end":1, "location":1, "day":1 }):
			
			reply += ("====================\n")
			reply += ("Type: " + x["nature"].title() + "\n")
			reply += ("Day: " + x["day"].title() + "\n")
			reply += ("Start: " + x["start"] + "\n")
			reply += ("End: " + x["end"] + "\n")
			reply += ("📍 " + x["location"].upper() + "\n")
		bot.send_message(chat_id=update.message.chat_id, text=reply)

def get_day(bot,update,args):
	if (len(args)==0):
		bot.send_message(chat_id=update.message.chat_id, text="🧒 Please enter /getday followed by a day")
		return
	day = args[0]
	if (timetable.count_documents({"day": day.lower()})==0):
		bot.send_message(chat_id=update.message.chat_id, text="😞 Day does not exist in database, please try again")
	else:
		bot.send_message(chat_id=update.message.chat_id, text="🧒 Getting information for: " + day.title())
		query ={"day": day.lower()}
		reply = ""
		reply += ("Day: " + day.title() + "\n")
		for x in timetable.find(query,{ "_id": 0,"name": 1, "nature": 1, "start":1, "end":1, "location":1, "code":1}).sort("start"):
			
			reply += ("====================\n")
			reply += ("🏫 " + x["code"].upper() + "\n")
			reply += ("Type: " + x["nature"].title() + "\n")
			
			reply += ("Start: " + x["start"] + "\n")
			reply += ("End: " + x["end"] + "\n")
			reply += ("📍 " + x["location"].upper() + "\n")
		bot.send_message(chat_id=update.message.chat_id, text=reply)