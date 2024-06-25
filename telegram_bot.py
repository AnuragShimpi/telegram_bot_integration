from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
import requests
from config import *
 
TOKEN: Final = telegram_api
# BOT_USERNAME: Final = '@GenElvebot'
 
# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am your go-to chatbot for instant weather updates and information searches, providing you with accurate and timely results.")
 
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""Hello! I am your go-to chatbot for instant weather updates and information searches. Here's how you can use me:
                                    \n\tWeather Updates: Just type "weather" followed by the city name (e.g., "weather in New York") to get the latest weather information.
                                    \n\tSearch Information: Ask me any question or search for any topic (e.g., "latest news on technology"), and I'll provide you with accurate and up-to-date results.
                                    \nIf you need further assistance, feel free to ask!""")
 
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command!')
 
# Handle response
 
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
 
    # print("message type :: ",message_type)
    
    print(f"user id :: ({update.message.chat.id}) user name :: ({update.message.chat.username})")
    print("text message :: ",text)
 
    result = call_search_api2(text)
    print('Bot:', result)
    await update.message.reply_text(result)
 
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")
 
 
base_url = "http://127.0.0.1:8000" # - query - result
 
# base_url = "https://webapp-be-nlq.azurewebsites.net"  # - input - output
 
def call_search_api2(query:str):
    payload = {"query": query}
    response = requests.post(f"{base_url}/search", json=payload)
    if response.status_code == 200:
        return response.json().get("result")
    else:
        return f"Failed to call search API: {response.status_code}, {response.text}"
 
 
# ------------------------------------------
 
 
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
 
    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
 
    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
 
    # Errors
    app.add_error_handler(error)
 
    # increased timeout for update
    print("Executing....")
    app.run_polling(poll_interval=3, timeout=10)  # Increased timeout to 10 seconds