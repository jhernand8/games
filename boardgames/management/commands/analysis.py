from django.core.management.base import BaseCommand, CommandError
from django.core.serializers.json import DjangoJSONEncoder
from urllib.request import urlopen
import json
import time
from boardgames.models import Boardgame
from bs4 import BeautifulSoup

# Command to fetch game list from boardgame geek
class Command(BaseCommand):
  def handle(self, *args, **options):
    allGames = Boardgame.objects.all();

    for size in range(1, 4):
      nGramCounter = {}
      for game in allGames:
        name = game.name.lower()

        for startInd in range(0, len(name) - size):
          ngram = name[startInd:startInd + size]
          if ngram not in nGramCounter:
            nGramCounter[ngram] = 0;
          nGramCounter[ngram] = nGramCounter[ngram] + 1;
    
      sortedCounter = sorted(nGramCounter.items(), key=lambda keyVal: keyVal[1]);
      for item in sortedCounter:
        if item[1] < 10:
          continue
        print(item[0] + ": " + str(item[1]));
      #for ng, c in nGramCounter.items():
        #print(ng + ": " + str(c))
      
