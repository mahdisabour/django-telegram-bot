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
from user.models import SiteBotMember
from django.conf import settings

from user.tasks import sendMessageFromBot



class TelegramSiteBot:
    def __init__(self):
        # Enable logging
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
        )
        self.logger = logging.getLogger(__name__)
        self.PHONE_NUMBER = range(1)
    
    def start(self, update: Update, _: CallbackContext) -> int:

        self.chat_id = update.message.chat_id
        
        if (SiteBotMember.objects.filter(chat_id=self.chat_id).exists()):
            update.message.reply_text(
                'این شماره قبلا در بات ثبت نام کرده است لازم نیست مجدد این کار را انجام دهید',
            )
            return ConversationHandler.END
            
        else:
            update.message.reply_text(
                'سلام . برای این که از خدمات بات تلگرام سایت استفاده کنید لطفا شماره تلفن خود را وارد کنید '
                'برای خارج شدن  /cancel را بفرستید\n\n'
                'لطفا شماره تلفن خود را وارد کنید',
            )
            return self.PHONE_NUMBER

    

    def phone_number(self, update: Update, _: CallbackContext) -> int:
        user = update.message.from_user
        self.logger.info("Phone Number of %s: %s", user.first_name, update.message.text)
        phone_number = update.message.text

        if(SiteBotMember.objects.filter(phone_number=phone_number).exists()):
            instance = SiteBotMember.objects.get(phone_number=phone_number)
            if (not instance.chat_id):
                instance.chat_id = self.chat_id
                instance.save()
                update.message.reply_text(
                    'شما اکنون از امکانات سایت بهره مند شده اید',
                )
            else:
                update.message.reply_text(
                    'این شماره قبلا در این بات ثبت نام کرده است',
                )
        else:
            update.message.reply_text(
                'کاربری با این شماره تلفن هنوز در سایت ثبت نام نکرده است لطفا ابتدا در سایت ثبت نام کنید و یک سفارش ثبت کنید',
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
            token=settings.TOKEN)
        # Get the dispatcher to register handlers
        dispatcher = updater.dispatcher
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],
            states={
                self.PHONE_NUMBER: [MessageHandler(Filters.text & ~Filters.command, self.phone_number)],
            },
            fallbacks=[CommandHandler('cancel', self.cancel)],
        )
        dispatcher.add_handler(conv_handler)
        updater.start_polling()
        updater.idle()


if __name__ == "__main__":
    print("hello bot")