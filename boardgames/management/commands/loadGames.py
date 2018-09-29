from django.core.management.base import BaseCommand, CommandError
from django.core.serializers.json import DjangoJSONEncoder
from urllib.request import urlopen
import json
import time
from bs4 import BeautifulSoup

# Command to fetch game list from boardgame geek
class Command(BaseCommand):
  def handle(self, *args, **options):

    baseUrl = "https://www.boardgamegeek.com/browse/boardgame/page/"
    for i in range(1, 11):
      url = baseUrl + str(i)
      print("url: " + url);
      resp = urlopen(url)
      html = BeautifulSoup(resp.read(), 'html.parser')
      try:
        table = html.find("table", id="collectionitems")
        rows = table.findAll("tr")

        # go thru each row in the table - each row representing a different game
        for currRow in rows:
          tdElems = currRow.find_all("td", attrs={"class": "collection_rank"});
          if len(tdElems) < 1:
            continue;
          nameTd = currRow.find_all("td", attrs={"class": "collection_objectname"})[0]; 
          nameA = nameTd.find("a");
          name = nameA.contents[0]
          
          rank = str(tdElems[0].text.strip());

          gameUrl = nameA['href'];
          print(str(rank) + ": " + name + ": " + gameUrl);
        time.sleep(3)
      except Exception as e:
        print(str(e) + "\n");
        continue;
