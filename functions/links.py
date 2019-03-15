syllabi={"key":"value"}

def syllabus(bot, update, args):   
	if (len(args)==0):
		bot.send_message(chat_id=update.message.chat_id, text="🧒 Please enter /syllabus followed by a major")
		return
	elif args[0].lower() in syllabi:
		#bot.send_message(chat_id=update.message.chat_id, text="Fetching: " + args[0])
		bot.send_document(chat_id=update.message.chat_id, document=syllabi[args[0].lower()])
	else:
		bot.send_message(chat_id=update.message.chat_id, text="Invalid course keyword") 


