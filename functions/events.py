import pymongo
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
client = pymongo.MongoClient("")
db = client[""]
events = db[""]
from datetime import datetime
def format_date(dt_string):
	try:
		return datetime.strptime(dt_string, "%d/%m/%Y").date()
	except:
		try: 
			return datetime.strptime(dt_string, "%d-%m-%Y").date()
		except:
			try: 
				return datetime.strptime(dt_string, "%d%m%Y").date()
			except:
				try: 
					return datetime.strptime(dt_string, "%d.%m.%Y").date()
				except:
					try: 
						return datetime.strptime(dt_string, "%d %b %Y").date()
					except:
						try: 
							return datetime.strptime(dt_string, "%d %B %Y").date()
						except:
							try: 
								return datetime.strptime(dt_string, "%d %B %y").date()
							except:
								try: 
									return datetime.strptime(dt_string, "%d %B").replace(datetime.today().year).date()
								except:
									return("invalid date")

def format_db_date(dt_string):
	return datetime.strptime(dt_string, "%Y-%m-%d").date().strftime("%d %B %Y")

def add_event(bot,update,args):
	fields = ['name:', "date:", "location:", "start:","end:","contact:"]
	fields_1 = ['name', "date", "location", "start","end","contact"]
	_in=args
	#default dictionary values of Nil
	_dict = {'name':'Nil','date':'Nil','location':'Nil','start':'Nil','end':'Nil','contact':'Nil'}
	#parser to get the values for each field, accounts for spaces between entries and fields.
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
	#take care of the white spaces if any, especially the ones added earlier
	name = _dict["name"].rstrip()
	date = str(format_date(_dict["date"].rstrip()))
	location  = _dict["location"].rstrip()
	start = _dict["start"].rstrip()
	end = _dict["end"].rstrip()
	contact = _dict["contact"].rstrip()
	if (events.count_documents({"name":name}) == 0):
		bot.send_message(chat_id=update.message.chat_id, text="👶 Adding new event: "+name.title())
		event_entry = { "name": name.lower(), "date": date, "location": location.lower(), "start": start, "end": end, "contact": contact.lower() }
		events.insert_one(event_entry)
	else:
		bot.send_message(chat_id=update.message.chat_id, text="🧒 Editing existing event: "+name.title())
		query = { "name": name.lower() }
		update = { "$set": { "date": date, "location": location.lower(), "start": start, "end": end, "contact": contact.lower() } }
		events.update_one(query, update)


def get_event(bot, update, args):  
	fields = ['name', "date", "location", "start","end","contact"]
	if (len(args)==0):
		bot.send_message(chat_id=update.message.chat_id, text="🧒 Please enter /getevent followed by an event name")
		return
	if args[-1] in fields:
		name = ""
		for i in range(len(args)-1):
			name += (args[i] + " ")
		name = name.rstrip()

		if (events.count_documents({"name": name.lower()})==0):
			bot.send_message(chat_id=update.message.chat_id, text="😞 Event does not exist in database, please try again")

		else:
			
			field = args[1].lower()
			query = {"name": name.lower()}
			output = events.find(query)
			answer = output[0][field]
			if (field == 'location' or field == 'date' or field == 'contact'):
				bot.send_message(chat_id=update.message.chat_id, text=answer.title())
			else:
				bot.send_message(chat_id=update.message.chat_id, text=answer)
	else:
		name = ""
		for i in range(len(args)):
			name += (args[i] + " ")
		name = name.rstrip()

		if (events.count_documents({"name": name.lower()})==0):
			bot.send_message(chat_id=update.message.chat_id, text="😞 Event does not exist in database, please try again")

		else:
			bot.send_message(chat_id=update.message.chat_id, text="🧒 Getting event information for: " + name.title())
			query ={"name": name.lower()}
			output = events.find(query)
			answer = output[0]

			reply = ""
			reply+=("Name: " + answer['name'].title() + "\n")
			reply+=("Date: " + format_db_date(answer['date']) + "\n")
			reply+=("Location: " + answer['location'].upper() + "\n")
			reply+=("Start: " + answer['start'] + "\n")
			reply+=("End: " + answer['end'] + "\n")
			reply+=("Contact: " +  answer['contact'].title() + "\n")
			bot.send_message(chat_id=update.message.chat_id, text=reply)
