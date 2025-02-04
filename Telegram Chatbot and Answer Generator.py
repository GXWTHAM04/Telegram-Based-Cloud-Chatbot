import telebot
import google.generativeai as genai

# Bot token from BotFather
bot = telebot.TeleBot("//your bot token", parse_mode=None)

# Configure Google Generative AI
genai.configure(api_key="//your api key")

# Generation configuration
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config)
convo = model.start_chat(history=[])

# Set only the /start and /help commands
commands = [
    telebot.types.BotCommand("start", "Start the bot"),
    telebot.types.BotCommand("help", "Get help using the bot"),
    telebot.types.BotCommand("about", "about our bot"),
    telebot.types.BotCommand("mybot", "list my bot"),

]
bot.set_my_commands(commands)

# Handlers for /start and /help
@bot.message_handler(commands=['start'])
def send_start(message):
    bot.reply_to(message, "Welcome to the bot.")

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """
Available commands:
/start - Start the bot
/help - Get help using the bot
/about - about our bot
/mybot - list my bot
You can also send me a message, and I'll try to respond!
if any quries contact: @Gowtham_1149
"""
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['about'])
def send_about(message):
    bot.reply_to(message, "This bot is designed to assist users with intelligent, AI-generated responses. Powered by Google Generative AI (Gemini 1.5), it combines advanced natural language processing with seamless interaction through the Telegram Bot API. Whether you're looking for answers, engaging conversations, or simply exploring AI capabilities, this bot is here to help. Developed using Python, it represents the latest in AI-driven communication. Feel free to ask anything or use the available commands to get started!")

@bot.message_handler(commands=['mybot'])
def send_mybot(message):
    bot.reply_to(message, "\\ your replays\n")

# Default handler for any other text messages
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        # Send message to the AI model
        convo.send_message(message.text)
        response = convo.last.text
        bot.reply_to(message, response)
    except Exception as e:
        bot.reply_to(message, f"Error processing your message: {str(e)}")

# Start polling
bot.infinity_polling()