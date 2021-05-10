from django.core.management.base import BaseCommand, CommandError
from user.bots.handleSiteBot import TelegramSiteBot


class Command(BaseCommand):
    help = "run telegram bot"


    def handle(self, *args, **kwargs):
        teleBot = TelegramSiteBot()
        teleBot.main()
        print("hello django bot")