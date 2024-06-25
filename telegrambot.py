import os
from config import *
import telebot
import os
import telebot
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
from langchain_cohere import ChatCohere
from langchain.chains import ConversationChain, LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import AgentType, initialize_agent
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

    

bot = telebot.TeleBot(telegram_api)

template = """Name of Assistant is Jarvis and it is a large language model trained by Cohere.

    Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

    Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

    Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

    Human: {human_input}
    Assistant:"""

prompt = PromptTemplate(
    input_variables=["human_input"], 
    template=template
)

agent_chain = LLMChain(
    llm=ChatCohere(cohere_api_key=cohere_api,
                model = 'command-r-plus' , 
                temperature=0),
                prompt=prompt, 
                verbose=True, 
                memory=ConversationBufferWindowMemory(k=2),
)


@bot.message_handler(['start'])
def Start(message):
    bot.reply_to(message, "Hello, How can I help you?") 

@bot.message_handler()
def chat(message):
    try:
        response = agent_chain.predict(human_input = message.text)
        bot.reply_to(message, response)
    except Exception as e:
        print(e)
        bot.reply_to(message, e)

print("bot started..")
bot.polling()