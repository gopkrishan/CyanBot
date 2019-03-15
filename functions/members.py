import pymongo
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
client = pymongo.MongoClient("")
db = client[""]
members = db[""]

#insert info needs name then fields in the format: name major number email birthday cca
def insert_info(bot,update,args):
	fields = ['name:', "email:", "major:", "cca:", "number:", "birthday:"]
	fields_1 = ['name', "email", "major", "cca", "number", "birthday"]
	_in=args
	_dict = {'name':'Nil','major':'Nil','email':'Nil','birthday':'Nil','cca':'Nil','number':'Nil'}
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
		
	name = _dict["name"].rstrip()
	major = _dict["major"].rstrip()
	number  = _dict["number"].rstrip()
	email = _dict["email"].rstrip()
	birthday = _dict["birthday"].rstrip()
	cca = _dict["cca"].rstrip()
	if (members.count_documents({"name":name}) == 0):
		bot.send_message(chat_id=update.message.chat_id, text="👶 Adding new member: "+name.title())
		member_entry = { "name": name.lower(), "email": email, "major": major.lower(), "number": number, "birthday": birthday, "cca": cca.lower() }
		members.insert_one(member_entry)
	else:
		bot.send_message(chat_id=update.message.chat_id, text="🧒 Editing existing member: "+name.title())
		query = { "name": name.lower() }
		update = { "$set": { "email": email, "major": major.lower(), "number": number, "birthday": birthday, "cca": cca.lower() } }
		members.update_one(query, update)

#get_info needs name and field: so *name* then email/major/cca/number/birthday
def get_info(bot, update, args):  
	if (len(args)==0):
		bot.send_message(chat_id=update.message.chat_id, text="🧒 Please enter /getmember followed by a name")
		return
	fields = ['name', "email", "major", "cca", "number", "birthday"]
	if args[-1] in fields:
		name = ""
		for i in range(len(args)-1):
			name += (args[i] + " ")
		name = name.rstrip()
	
		if (members.count_documents({"name": name.lower()})==0):
			bot.send_message(chat_id=update.message.chat_id, text="😞 Name does not exist in database, please try again")

		else:
			
			field = args[-1].lower()
			query = {"name": name.lower()}
			output = members.find(query)
			answer = output[0][field]
			if (field == 'major' or field == 'cca'):
				bot.send_message(chat_id=update.message.chat_id, text=answer.title())
			else:
				bot.send_message(chat_id=update.message.chat_id, text=answer)
	else:
		name = ""
		for i in range(len(args)):
			name += (args[i] + " ")
		name = name.rstrip()
		if (members.count_documents({"name": name.lower()})==0):
			bot.send_message(chat_id=update.message.chat_id, text="😞 Name does not exist in database, please try again")
		else:
			bot.send_message(chat_id=update.message.chat_id, text="🧒 Getting information for: " + name.title())
			query ={"name": name.lower()}
			output = members.find(query)
			answer = output[0]
			reply = ""
			reply+=("Name: " + answer['name'].title() + "\n")
			reply+=("Email: " + answer['email'] + "\n")
			reply+=("Major: " + answer['major'].title() + "\n")
			reply+=("Number: " + answer['number'] + "\n")
			reply+=("Birthday: " + answer['birthday'] + "\n")
			reply+=("CCA: " +  answer['cca'].title() + "\n")
			bot.send_message(chat_id=update.message.chat_id, text=reply)