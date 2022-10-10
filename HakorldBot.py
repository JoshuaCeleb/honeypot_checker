
from curses.ascii import isdigit
from distutils.archive_util import make_archive
from subprocess import call
from tkinter.messagebox import CANCEL
from unittest import findTestCases
from telegram import *
from telegram.ext import *
from web3 import Web3
from testBuyToken import *

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


def process_trade_options(update: Update, context: CallbackContext):
    sender_address = '0x8bb14E621648C822927B847FB09441a702d44782' # Enter your wallet address in this field
    private_key = "b3ebad94af464ea3fbd9fe5f10d54c4ecdc9c0bb4345213ff09dbbbfcce1716f"

    query = update.callback_query
    selection = query.data

    if selection == BUY_TOKEN:
        #query.answer()
        bsc = "https://bsc-dataseed.binance.org/"
        web3 = Web3(Web3.HTTPProvider(bsc))
        update.effective_message.reply_text("Welcome to the space")
        context.bot.send_message(chat_id=update.effective_chat.id, 
        text='Enter token contract address', reply_markup=ForceReply())
        return TOKEN_ADDRESS

    elif selection == CHECK_BALANCE:
        bsc = "https://bsc-dataseed.binance.org/"
        web3 = Web3(Web3.HTTPProvider(bsc))
        balance = web3.eth.get_balance("0x8bb14E621648C822927B847FB09441a702d44782")
        balances = web3.fromWei(balance, 'ether')
        update.effective_message.reply_text(f"Your current balance: {balances} BNB")
        return END_CONVERSATION


def process_token_address(update: Update, context: CallbackContext):
    global token_address
    token_address = update.message.text
    context.user_data['token_address'] = token_address
    update.message.reply_text(f'Token contract address is: {token_address[:100]}')
    context.bot.send_message(chat_id=update.effective_chat.id, 
        text='Enter amount you want to buy', reply_markup=ForceReply())

    return AMOUNT

def process_amount(update: Update, context: CallbackContext):
    global amount_tobuy
    amount_tobuy = update.message.text
    if amount_tobuy.isdigit():
        amount_tobuy = float(amount_tobuy)
        context.user_data['amount'] = amount_tobuy
        update.message.reply_text(f'Amount to buy is: {amount_tobuy} BNB')
    
        return CONFIRM
    else:
        update.message.reply_text('Invalid amount entered. Type /help to show trade options.')
        return END_CONVERSATION

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
def confirm_trade(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Confirm", callback_data=CONFIRM),
        InlineKeyboardButton("Cancel", callback_data=CANCEL)]
    ]

    update.message.reply_text(f"Confirm the trade: ", reply_markup=InlineKeyboardMarkup(keyboard))
    query = update.callback_query
    if query.data == CONFIRM:
        return PROCESS_TRADE

    else: 
        update.message.reply_text("Trade cancelled. Type /help to show trades options")

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
            TRADE_OPTIONS: [CallbackQueryHandler(process_trade_options, pass_user_data=True)],
            TOKEN_ADDRESS: [MessageHandler(filters=Filters.text, callback=process_token_address, pass_user_data=True)],
            AMOUNT: [MessageHandler(Filters.text, callback=process_amount, pass_user_data=True)],
            TAKE_PROFIT: [MessageHandler(Filters.text, callback=process_take_profit, pass_user_data=True)],
            STOP_LOSS: [MessageHandler(Filters.text, callback=process_stop_loss, pass_user_data=True)],
            CONFIRM: [CallbackQueryHandler(confirm_trade, pass_user_data=True)],
            PROCESS_TRADE: [CallbackQueryHandler(process_trade, pass_user_data=True)]
        },

    )
    return conversation_handler

updater.dispatcher.add_handler(CommandHandler('start', show_help))
updater.dispatcher.add_handler(build_conversation_handler())
updater.start_polling()

