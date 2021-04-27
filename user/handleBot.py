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

from django.core.exceptions import ValidationError
from .models import VipMembers

import user.telegramCalendar as telegramCalendar

class TelegramBot:
    def __init__(self):
        # Enable logging
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
        )

        self.logger = logging.getLogger(__name__)
        self.NAME, self.LAST_NAME, self.GENDER, self.BIRTH_DAY, self.PHONE_NUMBER, self.EMAIL , self.SKILL_LEVEL = range(7)

    
    def start(self, update: Update, _: CallbackContext) -> int:

        update.message.reply_text(
            'سلام . لطفا برای ثبت نام اطلاعات خود را وارد کنید '
            'برای خارج شدن از مکالمه /cancel را بفرستید\n\n'
            'لطفا نام خود را وارد کنید',
        )
        return self.NAME


    def name(self, update: Update, _: CallbackContext) -> int:
        user = update.message.from_user
        self.name = update.message.text
        self.logger.info("FirstName of %s: %s", user.first_name, update.message.text)
        update.message.reply_text(
            'لطفا نام خانوادگی خود را وارد کنید',
        )
        return self.LAST_NAME

    

    def last_name(self, update: Update, _: CallbackContext) -> int:
        reply_keyboard = [['مرد', 'زن', 'ناشناخته']]
        user = update.message.from_user
        self.last_name = update.message.text
        self.logger.info("LastName of %s: %s", user.first_name, update.message.text)
        update.message.reply_text(
            'لطفا جنسیت خود را انتخاب کنید',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
        return self.GENDER




    def gender(self, update: Update, _: CallbackContext) -> int:
        user = update.message.from_user
        self.logger.info("Gender of %s: %s", user.first_name, update.message.text)
        self.gender = update.message.text
        update.message.reply_text(
            'لطفا تاریخ تولد خود را انتخاب کنید',
            reply_markup=ReplyKeyboardRemove(),
        )
        return self.B


    def birth_day(self, update: Update, _: CallbackContext) -> int:
        user = update.message.from_user
        self.logger.info("Email Number of %s: %s", user.first_name, update.message.text)
        self.email = update.message.text
        update.message.reply_text(
            'لطفا شماره تلفن همراه خود را وارد کنید',
            reply_markup=ReplyKeyboardRemove(),
        )
        return self.SKILL_LEVEL

    
    def phone_number(self, update: Update, _: CallbackContext) -> int:
        user = update.message.from_user
        self.logger.info("Phone Number of %s: %s", user.first_name, update.message.text)
        self.phone_number = update.message.text

        # validate Phone Number

        update.message.reply_text(
            'لطفا ایمیل خود را وارد کنید',
        )
        return self.EMAIL

    def email(self, update: Update, _: CallbackContext) -> int:
        reply_keyboard = [['مبتدی', 'متوسط', 'پیشرفته']]
        user = update.message.from_user
        self.logger.info("Email Number of %s: %s", user.first_name, update.message.text)
        self.email = update.message.text
        update.message.reply_text(
            'لطفا میزان مهارت خود را انتخاب کنید',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
        return self.SKILL_LEVEL


    

    def skill_level(self, update: Update, _: CallbackContext) -> int:
        user = update.message.from_user
        self.logger.info("Skill of %s: %s", user.first_name, update.message.text)
        self.skill_level = update.message.text
        
        genderDict = {"مرد": "male", "زن": "female", "ناشناخته": "unknown"}
        skillLevelDict = {"مبتدی": "beginner", "متوسط": "intermediate", "پیشرفته": "advanced"}


        print(VipMembers.objects.filter(phone_number=self.phone_number).exists())


        instance = None
        if not VipMembers.objects.filter(phone_number=self.phone_number).exists(): 
            instance = VipMembers.objects.create(
                name=self.name, last_name=self.last_name, gender=genderDict[self.gender],phone_number=self.phone_number ,email=self.email, skill_level=skillLevelDict[self.skill_level]
            )
        else:
            update.message.reply_text(
                'مشترک با این شماره همراه قبلا ثبت نام کرده است',
                reply_markup=ReplyKeyboardRemove(),
            )
            return ConversationHandler.END


        

        try:
            instance.full_clean()
            instance.save()
            update.message.reply_text(
                'اطلاعات شما ذخیره شد . با تشکر',
                reply_markup=ReplyKeyboardRemove(),
            )

        except ValidationError as e:
            print(e)
            update.message.reply_text(
                'لطفا اطلاعات درست را وارد نمایید',
                reply_markup=ReplyKeyboardRemove(),
            )

        return ConversationHandler.END


    def cancel(self, update: Update, _: CallbackContext) -> int:
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
                self.GENDER: [MessageHandler(Filters.regex('^(مرد|زن|ناشناخته)$'), self.gender)],
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
