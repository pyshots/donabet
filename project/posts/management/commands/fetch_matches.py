from django.core.management.base import BaseCommand
from posts.utils.api_football import fetch_and_save_partidos

class Command(BaseCommand):
    help = 'Fetch and save matches from Football-Data.org'

    def handle(self, *args, **kwargs):
        fetch_and_save_partidos()
        self.stdout.write(self.style.SUCCESS('Matches fetched and saved successfully'))