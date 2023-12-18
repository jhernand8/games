from django.core.management.base import BaseCommand, CommandError
from django.core.serializers.json import DjangoJSONEncoder
import json
import pytz
from boardgames.models import TopStoryIdsByTime
from boardgames.models import HNStory
from boardgames.models import HNTopStory
from boardgames import storyutils
from datetime import date
from datetime import datetime
from datetime import timedelta
from pytz import timezone

# Cron job that looks at the top story ids that we have saved
# and combines them into a single list
# and fetches the stories saving them to the db in
# as HNTopStory.
class Command(BaseCommand):
  # Checks whether or not this program should run -
  # based on the current time.
  def shouldUpdate(self):
    currTime = datetime.utcnow()
    currTimeUTC = pytz.utc.localize(currTime)
    pacificTZ = timezone("US/Pacific")
    pacificTime = currTimeUTC.astimezone(pacificTZ)
    hour = pacificTime.hour
    min = pacificTime.minute
    if hour > 5 and hour <= 13:   
      return True;
    if hour >= 17 and hour <= 21:
      return True;
    return False

  def handle(self, *args, **options):
    if not self.shouldUpdate() :
      print("Exiting - not in window to run.\n");
      return

    prevTop = HNTopStory.objects.all()

    topIds = TopStoryIdsByTime.objects.all()
    uniqueIds = set()
    for topIdsForTime in topIds:
      ids = json.loads(topIdsForTime.storyIds)
      for currid in ids:
        try:
          uniqueIds.add(int(currid))
        except:
          pass;
    print("number of unique ids: " + str(len(uniqueIds)) + ".\n")
 
    # remove previous top ones that are in the current set
    # record deleted ones so we don't add them back
    for prevStory in prevTop:
      previd = json.loads(prevStory.story).get('id')
      if int(previd) in uniqueIds:
        if prevStory.marked_deleted is True:
          uniqueIds.remove(int(previd))
        else:
          prevStory.delete()
    # now fetch stories
    for id in uniqueIds:
      story = storyutils.get_item(id)
      try:
        if storyutils.is_deleted(story):
          continue
      except:
        continue;
      score = story.get('score')
      if score == 1:
        continue
      topStory = HNTopStory(hnStoryId = int(id), story = json.dumps(story, cls=DjangoJSONEncoder))
      topStory.save()

    # now delete top ids
    for topIdsForTime in TopStoryIdsByTime.objects.all():
      topIdsForTime.delete()

    # also remove old top stories, ie more than n days old
    for prevStory in prevTop:
      if int(json.loads(prevStory.story).get('id')) in uniqueIds:
        continue
      daysOld = timedelta(days = 21)
      if (prevStory.date + daysOld) < date.today():
        prevStory.delete()
      # also delete stories based on submission date - as sometimes these
      # will later make it back into the top 100 stories
      else:
        storyTime = int(json.loads(prevStory.story).get('time'))
        storyDate = datetime.fromtimestamp(storyTime).date()
        if (storyDate + daysOld + daysOld) < date.today():
          prevStory.delete()


