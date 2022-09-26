from subprocess import call
from tkinter.messagebox import CANCEL
from telegram import *
from telegram.ext import *
from BuyToken import *

updater = Updater("5743525345:AAEJeEJC8kriVlS5wbJYELyoXWrSoLap_AA",
                  use_context=True)

TRADE_OPTIONS = "trade_options"
BUY_TOKEN = "buy_token"
SELL_TOKEN = "sell_token"
TOKEN_ADDRESS = "token_address"
AMOUNT = "amount"
TAKE_PROFIT = "take_profit"
STOP_LOSS = "stop_loss"
CONFIRM = "confirm"
CHECK_BALANCE = "check_balance"
PLACED_TRADES = "placed_trades"
PROCESS_TRADE = "process_trade"
END_CONVERSATION = ConversationHandler.END

def show_help(update: Update, context: CallbackContext):
    update.message.reply_text('Type /help to show trade options')

def show_options(update: Update, context: CallbackContext):
    button_list = [
        [InlineKeyboardButton("Buy Token", callback_data=BUY_TOKEN),
        InlineKeyboardButton("Sell Token", callback_data=SELL_TOKEN)],
        [InlineKeyboardButton("Available Balance", callback_data=CHECK_BALANCE),
        InlineKeyboardButton("Placed trades", callback_data=PLACED_TRADES)]
    ]
    update.effective_message.reply_text("Trade options:", reply_markup=InlineKeyboardMarkup(button_list))
    return TRADE_OPTIONS

"""def callback_button(update: Update, context: CallbackContext):
    selection = update.callback_query.data
    if selection == SELL_TOKEN:
        buyTokens"""

def process_trade_option(update: Update, context: CallbackContext, user_data):
    query = update.callback_query
    selection = query.data

    if selection == BUY_TOKEN:
        user_data[TRADE_OPTIONS] = update.message.text
        update.message.reply_text(f'Enter token adress you want to buy: {user_data[TRADE_OPTIONS]}')
        return TOKEN_ADDRESS 

def process_token_address(update: Update, context: CallbackContext, user_data):
    user_data[TOKEN_ADDRESS] = update.message.text()
    update.message.reply_text(f'What amount of {user_data[TOKEN_ADDRESS]}')
    return AMOUNT

def process_amount(update: Update, context: CallbackContext, user_data):
    user_data[AMOUNT] = float(update.message.text)
    update.message.reply_text(f'What % profit for {user_data[AMOUNT]} {user_data[TOKEN_ADDRESS]}')
    return TAKE_PROFIT

def process_take_profit(update: Update, context: CallbackContext, user_data):
    user_data[TAKE_PROFIT] = float(update.message.text)
    update.message.reply_text(f'What % loss  for {user_data[AMOUNT]} {user_data[TOKEN_ADDRESS]}')
    return STOP_LOSS

def process_stop_loss(update: Update, context: CallbackContext, user_data):
    user_data[STOP_LOSS] = float(update.message.text)

    keyboard = [
        [InlineKeyboardButton("Confirm", callback_data=CONFIRM),
        InlineKeyboardButton("Cancel", callback_data=CANCEL)]
    ]

    update.message.reply_text(f"Confirm the trade: ",
                                reply_markup=InlineKeyboardMarkup(keyboard))
    return PROCESS_TRADE

def  process_trade(update: Update, context: CallbackContext, user_data):
    query = update.callback_query

    if query.data == CONFIRM:
        trade = buyTokens()
        buyTokens()
        update.callback_query.message.reply_text(f'Scheduled: {trade}')
    else:
        CommandHandler("start", callback=show_help)

    return END_CONVERSATION


def build_conversation_handler():
    entry_handler = CommandHandler("help", callback=show_options)
    conversation_handler = ConversationHandler(
        entry_points=[entry_handler],
        fallbacks=[entry_handler],
        states={
            TRADE_OPTIONS: [CallbackQueryHandler(process_trade_option, pass_user_data=True)],
            TOKEN_ADDRESS: [MessageHandler(filters=Filters.text, callback=process_token_address, pass_user_data=True)],
            AMOUNT: [MessageHandler(Filters.text, callback=process_amount, pass_user_data=True)],
            TAKE_PROFIT: [MessageHandler(Filters.text, callback=process_take_profit, pass_user_data=True)],
            STOP_LOSS: [MessageHandler(Filters.text, callback=process_stop_loss, pass_user_data=True)],
            PROCESS_TRADE: [CallbackQueryHandler(process_trade, pass_user_data=True)]
        },

    )
    return conversation_handler

updater.dispatcher.add_handler(CommandHandler('start', show_help))
updater.dispatcher.add_handler(CommandHandler('help', callback=show_options))
updater.dispatcher.add_handler(build_conversation_handler())
updater.start_polling()


@staticmethod
def build_trade(user_data):
    current_trade = user_data[TRADE_OPTIONS]
    token_address = user_data[TOKEN_ADDRESS]
    amount = user_data[AMOUNT]
    take_profit = user_data[TAKE_PROFIT]

    if current_trade == BUY_TOKEN:
        return buyTokens(amount, token_address, take_profit)
    else:
        raise NotImplementedError
        