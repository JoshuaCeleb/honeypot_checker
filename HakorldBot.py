from subprocess import call
from telegram import *
from telegram.ext import *
from BuyToken import *

updater = Updater("5743525345:AAEJeEJC8kriVlS5wbJYELyoXWrSoLap_AA",
                  use_context=True)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Welcome to Hakorld DeFi Bot. Please write \
        /help to see list of available commands")



def help(update: Update, context: CallbackContext):
    update.message.reply_text(
        """/BuyTokens To buy a token
           /SellTokens to sell a token
        """
    )

    
        
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('BuyTokens', buyTokens))
updater.start_polling()