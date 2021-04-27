from django.core.management.base import BaseCommand, CommandError
from user.handleBot import TelegramBot


class Command(BaseCommand):
    help = "run telegram bot"


    def handle(self, *args, **kwargs):
        teleBot = TelegramBot()
        teleBot.main()
        print("hello django bot")