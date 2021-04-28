import logging
import jdatetime
import datetime

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

from .tasks import sendMessageFromBot



class TelegramBot:
    def __init__(self):
        # Enable logging
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
        )
        self.logger = logging.getLogger(__name__)
        self.NAME, self.LAST_NAME, self.GENDER, self.DATE_TYPE, self.BIRTH_YEAR, self.BIRTH_MONTH, self.BIRTH_DAY, self.PHONE_NUMBER, self.EMAIL , self.SKILL_LEVEL = range(10)
        self.birthConfigDict = {"year": "", "month": "", "day": ""}
    
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
        self.chat_id = update.message.chat_id
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
        reply_keyboard = [['میلادی', 'شمسی']]
        user = update.message.from_user
        self.logger.info("Gender of %s: %s", user.first_name, update.message.text)
        self.gender = update.message.text
        update.message.reply_text(
            'لطفا تقویم خود برای وارد کردن تاریخ تولد خود را انتخاب کنید',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
        return self.DATE_TYPE

    
    def date_type(self, update: Update, _: CallbackContext) -> int:
        user = update.message.from_user
        self.logger.info("Date Type of %s: %s", user.first_name, update.message.text)
        self.date_type = update.message.text
        update.message.reply_text(
            'لطفا سال تاریخ تولد خود را وارد کنید',
            reply_markup=ReplyKeyboardRemove(),
        )
        return self.BIRTH_YEAR



    def birth_year(self, update: Update, _: CallbackContext) -> int:
        user = update.message.from_user
        self.logger.info("Birth day(year) of %s: %s", user.first_name, update.message.text)
        self.birthConfigDict["year"] = update.message.text
        update.message.reply_text(
            'لطفا ماه تاریخ تولد خود را وارد کنید',
        )
        return self.BIRTH_MONTH



    def birth_month(self, update: Update, _: CallbackContext) -> int:
        user = update.message.from_user
        self.logger.info("Birth day(month) of %s: %s", user.first_name, update.message.text)
        self.birthConfigDict["month"] = update.message.text
        update.message.reply_text(
            'لطفا روز تاریخ تولد خود را وارد کنید',
        )
        return self.BIRTH_DAY



    def birth_day(self, update: Update, _: CallbackContext) -> int:
        user = update.message.from_user
        self.logger.info("Birth day(day) of %s: %s", user.first_name, update.message.text)
        self.birthConfigDict["day"] = update.message.text
        update.message.reply_text(
            'لطفا شماره تلفن همراه خود را وارد کنید',
        )
        return self.PHONE_NUMBER

    

    def phone_number(self, update: Update, _: CallbackContext) -> int:
        user = update.message.from_user
        self.logger.info("Phone Number of %s: %s", user.first_name, update.message.text)
        self.phone_number = update.message.text
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
        instance = None
        if not VipMembers.objects.filter(phone_number=self.phone_number).exists():
            # handle birthday convert
            try:
                if self.date_type == 'شمسی':
                    time = jdatetime.date(
                        int(self.birthConfigDict["year"]), 
                        int(self.birthConfigDict["month"]), 
                        int(self.birthConfigDict["day"]) 
                    ).togregorian()
                else:
                    time = datetime.datetime(
                        int(self.birthConfigDict["year"]), 
                        int(self.birthConfigDict["month"]), 
                        int(self.birthConfigDict["day"]))
            except Exception as e:
                print(e)
                update.message.reply_text(
                    'لطفا تاریخ تولد خود را به درستی وارد کنید',
                    reply_markup=ReplyKeyboardRemove(),
                )
                return ConversationHandler.END


            try: 
                instance = VipMembers(
                    name=self.name, last_name=self.last_name, gender=genderDict[self.gender],
                    phone_number=self.phone_number ,email=self.email, skill_level=skillLevelDict[self.skill_level],
                    date_of_birth= time, telegram_id= self.chat_id
                )
            except Exception as e:
                print(e)
                print("here error")
                update.message.reply_text(
                    'لطفا اطلاعات درست را وارد نمایید',
                    reply_markup=ReplyKeyboardRemove(),
                )
                return ConversationHandler.END
        else:
            update.message.reply_text(
                'مشترک با این شماره همراه قبلا ثبت نام کرده است',
                reply_markup=ReplyKeyboardRemove(),
            )
            return ConversationHandler.END
        try:
            instance.full_clean()
            instance.save()
            sendMessageFromBot.delay(telegram_id = self.chat_id)
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
                self.DATE_TYPE: [MessageHandler(Filters.regex('^(میلادی|شمسی)$'), self.date_type)],
                self.BIRTH_YEAR: [MessageHandler(Filters.text & ~Filters.command, self.birth_year)],
                self.BIRTH_MONTH: [MessageHandler(Filters.text & ~Filters.command, self.birth_month)],
                self.BIRTH_DAY: [MessageHandler(Filters.text & ~Filters.command, self.birth_day)],
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