import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)



class TelegramBot:
    def __init__(self):
        # Enable logging
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
        )

        self.logger = logging.getLogger(__name__)
        self.NAME, self.LAST_NAME, self.GENDER, self.PHONE_NUMBER, self.EMAIL, self.SKILL_LEVEL = range(6)

    
    def start(self, update: Update, _: CallbackContext) -> int:

        update.message.reply_text(
            'سلام . لطفا برای ثبت نام اطلاعات خود را وارد کنید '
            'برای خارج شدن از مکالمه /cancel را بفرستید\n\n'
            'لطفا نام خود را وارد کنید',
        )
        return self.NAME


    def name(self, update: Update, _: CallbackContext) -> int:
        user = update.message.from_user
        self.logger.info("FirstName of %s: %s", user.first_name, update.message.text)
        update.message.reply_text(
            'لطفا نام خانوادگی خود را وارد کنید',
        )
        return self.LAST_NAME

    

    def last_name(self, update: Update, _: CallbackContext) -> int:
        reply_keyboard = [['پسر', 'دختر', 'ناشناخته']]
        user = update.message.from_user
        self.logger.info("LastName of %s: %s", user.first_name, update.message.text)
        update.message.reply_text(
            'لطفا جنسیت خود را انتخاب کنید',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
        return self.GENDER


    def gender(self, update: Update, _: CallbackContext) -> int:
        user = update.message.from_user
        self.logger.info("Gender of %s: %s", user.first_name, update.message.text)
        update.message.reply_text(
            'لطفا شماره تلفن همراه خود را وارد کنید',
            reply_markup=ReplyKeyboardRemove(),
        )
        return self.EMAIL

    
    def phone_number(self, update: Update, _: CallbackContext) -> int:
        user = update.message.from_user
        self.logger.info("Phone Number of %s: %s", user.first_name, update.message.text)
        update.message.reply_text(
            'لطفا ایمیل خود را به درستی وارد کنید',
        )
        return self.PHONE_NUMBER

    def email(self, update: Update, _: CallbackContext) -> int:
        reply_keyboard = [['مبتدی', 'متوسط', 'پیشرفته']]
        user = update.message.from_user
        self.logger.info("Email Number of %s: %s", user.first_name, update.message.text)
        update.message.reply_text(
            'لطفا میزان مهارت خود را انتخاب کنید',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
        return self.SKILL_LEVEL

    def skill_level(self, update: Update, _: CallbackContext) -> int:
        user = update.message.from_user
        self.logger.info("Skill of %s: %s", user.first_name, update.message.text)
        update.message.reply_text(
            'اطلاعات شما ذخیره شد . با تشکر',
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END


    def cancel(update: Update, _: CallbackContext) -> int:
        user = update.message.from_user
        self.logger.info("User %s canceled the conversation.", user.first_name)
        update.message.reply_text(
            'خدانگهدار', reply_markup=ReplyKeyboardRemove()
        )

        return ConversationHandler.END

    

    def main(self):
        # Create the Updater and pass it your bot's token.
        updater = Updater(
            token='1633187717:AAGKkj3HmWy4qs3WQtnWz8mqhdOzoICUiLI')

        # Get the dispatcher to register handlers
        dispatcher = updater.dispatcher

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],
            states={
                self.NAME: [MessageHandler(Filters.text & ~Filters.command, self.name)],
                self.LAST_NAME: [MessageHandler(Filters.text & ~Filters.command, self.last_name)],
                self.GENDER: [MessageHandler(Filters.regex('^(پسر|دختر|ناشناخته)$'), self.gender)],
                self.PHONE_NUMBER: [MessageHandler(Filters.text & ~Filters.command, self.phone_number)],
                self.EMAIL: [MessageHandler(Filters.text & ~Filters.command, self.email)],
                self.SKILL_LEVEL: [MessageHandler(Filters.regex('^(مبتدی|متوسط|پیشرفته)$'), self.skill_level)],
                
            },
            fallbacks=[CommandHandler('cancel', self.cancel)],
        )

        dispatcher.add_handler(conv_handler)
        updater.start_polling()
        updater.idle()




if __name__ == "__main__":
    print("hello bot")




    

        
    



    


















# class TelegramBot:

#     def __init__(self):
#         # upadate and dispatcher to handle command and message
#         self.updater = Updater(
#             token='1633187717:AAGKkj3HmWy4qs3WQtnWz8mqhdOzoICUiLI', use_context=True)
#         self.dispatcher = self.updater.dispatcher
#         self.stateFlag = 0


#     def run(self):

#         logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                             level=logging.INFO)
#         # handle start command
#         start_handler = CommandHandler('start', self.start)
#         self.dispatcher.add_handler(start_handler)

#         # Start bot
#         self.updater.start_polling()


#     def start(self, update, context):
        
#         context.bot.send_message(
#             chat_id=update.effective_chat.id, text="Welcome to this bot \nPlease Enter your first name")

#         # handle message when start command sending
#         self.echo_handler = MessageHandler(Filters.text & (~Filters.command), self.echo)
#         self.dispatcher.add_handler(self.echo_handler)


#     def echo(self, update, context):
#         user_id = update.message.from_user['username']
#         print(user_id)
#         if not self.stateFlag:
#             self.FirstName = update.message.text 
#             context.bot.send_message(
#                 chat_id=update.effective_chat.id, text=f"Please enter your last name")
#             self.stateFlag = 1 
#         else:
#             self.LastName = update.message.text
#             context.bot.send_message(
#                 chat_id=update.effective_chat.id, text=f"We will register you\nGoodBye")

#             self.dispatcher.remove_handler(self.echo_handler)
#             self.stateFlag = 0

#             # save user data on django models
#             UserBot(first_name= self.FirstName, last_name= self.LastName).save() 
