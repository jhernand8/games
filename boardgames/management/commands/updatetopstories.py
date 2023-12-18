from django.core.management.base import BaseCommand, CommandError
from django.core.serializers.json import DjangoJSONEncoder
import json
from boardgames.models import TopStoryIdsByTime
from boardgames import storyutils

# Cron job that runs hourly or so that requests
# the ids of the current top stories on Hacker News
# and saves them to the dabase in TopStoryIdsByTime.
class Command(BaseCommand):
  
  def handle(self, *args, **options):
    topItemJSON = storyutils.get_top_items()
    topStories = TopStoryIdsByTime(storyIds = json.dumps(topItemJSON, cls=DjangoJSONEncoder))
    topStories.save()
