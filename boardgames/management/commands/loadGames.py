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

          # extract bgg id
          bggId = gameUrl[11:]
          bggId = bggId[0:bggId.find("/")]
          self.loadGameData(bggId)
        time.sleep(3)
      except Exception as e:
        print(str(e) + "\n");
        continue;


  # Method to use the xml api to load more data about a game - given its BGG id
  def loadGameData(self, bggId):
    #https://www.boardgamegeek.com/xmlapi2/thing?type=boardgame&id=144733&stats=1
    url = 'https://www.boardgamegeek.com/xmlapi2/thing?type=boardgame&id=' + str(bggId) + '&stats=1'
    htmlResp = urlopen(url)
    xml = BeautifulSoup(htmlResp.read(), 'xml')

    # weight
    weight = xml.find("averageweight")['value']
    # rating
    overallRating = xml.find("average")['value']
    # how many ratings
    numRatings = xml.find("usersrated")['value']

    print("   " + str(weight) + ": " + str(overallRating) + ":" + str(numRatings))
