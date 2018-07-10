from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from . import conf, lang, message

import telegram, logging

# Debug
#lvl = logging.DEBUG

# Production
lvl = logging.INFO

logging.basicConfig(level=lvl, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


def lang_config(bot, update, args):	
	global lang
	
	if not args:
		msg = message[lang]['lang_status']['use']

	elif args[0] == "pt-br" or args[0] == "pt-BR":
		lang = "ptbr"
		msg = message[lang]['lang_status']['success'].format(l=lang)

	elif args[0] == "EN" or args[0] == "en":
		lang = "en"
		msg = message[lang]['lang_status']['success'].format(l=lang)

	else:
		msg = message[lang]['lang_status']['error'].format(iso=args)

	bot.sendMessage(chat_id=update.message.chat_id, text=msg)

#start bot
def start(bot, update):
	msg = message[lang]['start']

	bot.sendMessage(chat_id=update.message.chat_id, text=msg.format(nickname=update.message.from_user['username']))


# Listagem de comandos disponíveis
def help(bot, update):
	msg = message[lang]['help']
	
	keyboard = [
		[
			telegram.KeyboardButton(
				"/regras",
				callback_data='rules')
		],
	]

	reply_markup = telegram.ReplyKeyboardMarkup(keyboard, resize_keyboard=True, selective=True)
	bot.sendMessage(chat_id=update.message.chat_id, text=msg, reply_markup=reply_markup)


# Boas vindas aos novos membros
def welcome(bot, update):
	msg=message[lang]['welcome']

	keyboard = [
        [
        	InlineKeyboardButton(
        		"Formulário da F3rBs",
        		callback_data="form")
        	,
        	InlineKeyboardButton(
        		"Sobre a F3rBs",
        		callback_data="f3rbs")
        ],
        [
            InlineKeyboardButton(
                "Nossa Redes", 
                callback_data='network')
        ],
        [
        	InlineKeyboardButton(
        		"Hacker/Maker space?",
        		callback_data="hmspace")
        ],
    ]

	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_message(chat_id=update.message.chat_id, text=msg.format(name=update.message.new_chat_members[0].full_name), reply_markup=reply_markup)


def bye(bot, update):
	msg = message[lang]['bye'].format(name=update.message.left_chat_member.full_name)

	update.message.reply_text(msg)


def error(bot, update, error):
	if error.message == "Forbidden: bot can't initiate conversation with a user":
		update.message.reply_text(text=message[lang]['error']['initiate'])
	elif error.message == "Forbidden: bot was blocked by the user":
		update.message.reply_text(text=message[lang]['error']['blocked'])
	else:
		logger.warning('Update "%s" caused error "%s"', update, error)

# Regras
def rules(bot, update):
	msg = message[lang]['rules']['title']

	for i in range(1,len(message[lang]['rules']) - 1):
		msg += "\n"
		msg += "*{number}* - {description}".format(number=i,description=message[lang]['rules'][str(i)])

	msg	+= message[lang]['rules']['ass']


	bot.sendMessage(chat_id=update.message.from_user.id, text=msg, parse_mode="Markdown")


# Retorno dos botões
def button(bot, update):
    query = update.callback_query
    
    if query.data == "network":
        bot.answer_callback_query(
            callback_query_id=query.id,
            text=('Site: f3rbshs.github.io\nAcervo: @rF3rBs\nRepositório: github.com/f3rbshs\nPágina: fb.com/f3rbshs'),
            show_alert=True
		)

    elif query.data == "hmspace":
    	msg = message[lang]['about'][query.data]['title']
    	msg += message[lang]['about'][query.data]['description']

    	bot.sendMessage(chat_id=query.from_user.id, text=msg)
    
    elif query.data == 'form':
    	msg = message[lang]['links']['form']

    	bot.sendMessage(chat_id=query.from_user.id, text=msg, parse_mode="Markdown")

    elif query.data == 'f3rbs':
    	bot.answer_callback_query(
    		callback_query_id=query.id,
    		text="Em breve",
    		show_alert=True)

    elif query.data == 'rules':
    	bot.answer_callback_query(callback_query_id=query.id)


def info(bot, update):
	msg = message[lang]['about']['info'].format(major=conf['bot']['version']['major'],minor=conf['bot']['version']['minor'],path=conf['bot']['version']['path'])

	bot.sendMessage(chat_id=update.message.chat_id, text=msg)

def main():
	updater = Updater(token=conf['bot']['token'])
	dispatcher = updater.dispatcher

	dispatcher.add_handler(CommandHandler('start', start))
	dispatcher.add_handler(CommandHandler('regras', rules))
	dispatcher.add_handler(CommandHandler('ajuda', help))
	dispatcher.add_handler(CommandHandler('info', info))
	dispatcher.add_handler(CommandHandler('lang', lang_config, pass_args=True))
#	dispatcher.add_handler(CommandHandler('enquete', survey, pass_args=True))
	dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
	dispatcher.add_handler(MessageHandler(Filters.status_update.left_chat_member, bye))
	dispatcher.add_handler(CallbackQueryHandler(button))
	dispatcher.add_error_handler(error)

	# Inicia o bot
	updater.start_polling()

	# Run the bot until the user presses Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT
	updater.idle()
