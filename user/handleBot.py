from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler, MessageHandler, Filters
from user.models import UserBot


class TelegramBot:

    def __init__(self):
        # upadate and dispatcher to handle command and message
        self.updater = Updater(
            token='1633187717:AAGKkj3HmWy4qs3WQtnWz8mqhdOzoICUiLI', use_context=True)
        self.dispatcher = self.updater.dispatcher

        self.stateFlag = 0


    def run(self):

        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        # handle start command
        start_handler = CommandHandler('start', self.start)
        self.dispatcher.add_handler(start_handler)

        # Start bot
        self.updater.start_polling()


    def start(self, update, context):
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Welcome to this bot \nPlease Enter your first name")

        # handle message when start command sending
        self.echo_handler = MessageHandler(Filters.text & (~Filters.command), self.echo)
        self.dispatcher.add_handler(self.echo_handler)


    def echo(self, update, context):
        if not self.stateFlag:
            self.FirstName = update.message.text 
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=f"Please enter your last name")
            self.stateFlag = 1 
        else:
            self.LastName = update.message.text
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=f"We will register you\nGoodBye")

            self.dispatcher.remove_handler(self.echo_handler)
            self.stateFlag = 0

            # save user data on django models
            UserBot(first_name= self.FirstName, last_name= self.LastName).save() 
