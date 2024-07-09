from config import *
import telebot
from langchain_cohere import ChatCohere
from langchain.chains import ConversationChain
from langchain_core.prompts import PromptTemplate
from langchain.chains.conversation.memory import ConversationBufferMemory

    
bot = telebot.TeleBot(telegram_api)

template = """Name of Assistant is Jarvis and it is a large language model trained by Cohere.

Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

Previous conversation history:
{history}

Human: {human_input}
Assistant:"""

prompt = PromptTemplate(
    input_variables=["history", "human_input"], 
    template=template
)

llm = ChatCohere(cohere_api_key=cohere_api, model='command-r-plus', temperature=0)

# Ensure the prompt is passed to the ConversationChain
memory = ConversationBufferMemory()
conversation_buf = ConversationChain(
    llm=llm,
    prompt=prompt,
    memory=memory,
    input_key="human_input",
    output_key="response"
)

@bot.message_handler(commands=['start'])
def Start(message):
    bot.reply_to(message, "Hello, How can I help you?") 

@bot.message_handler()
def chat(message: str):
    try:
        response = conversation_buf.run({"human_input": message.text})
        print("Generated response: ", response)
        bot.reply_to(message, response)
    except Exception as e:
        print(e)
        bot.reply_to(message, str(e))

print("bot started..")
bot.polling()