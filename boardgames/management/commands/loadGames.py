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
    maxNumPages = 40;
    baseUrl = "https://www.boardgamegeek.com/browse/boardgame/page/"
    allGames = Boardgame.objects.all();

    for i in range(1, maxNumPages):
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

          # extract bgg id
          bggId = gameUrl[11:]
          bggId = bggId[0:bggId.find("/")]

          # see if it exists, and if so, we will update the game
          if self.existsGameWithBGGId(int(bggId), allGames):
            game = self.gameWithBGGId(int(bggId), allGames)
            game.ranking = int(rank)
          else:
            game = Boardgame(name = name, ranking = int(rank), bggId = int(bggId), bggUrl = gameUrl); 

          game = self.loadGameData(bggId, game)
          print("   " + str(rank) + ": " + name + ": " + gameUrl);

          game.save()
          time.sleep(3);
        time.sleep(3)
      except Exception as e:
        print(str(e) + "\n");
        continue;


  # Method returns true if there is a boardgame entry in the list
  # with the given bggId, false otherwise.
  def existsGameWithBGGId(self, bggId, games):
    for game in games:
      if game.bggId == bggId:
        return True
    return False
  
  # Returns the game with the given bggId.
  def gameWithBGGId(self, bggId, games):
    for game in games:
      if game.bggId == bggId:
        return game
    return None

  # Method to use the xml api to load more data about a game - given its BGG id
  def loadGameData(self, bggId, game):
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

    game.complexityWeight = float(weight)
    game.rating = float(overallRating)
    game.numRatings = int(numRatings)
    game.playTime = int(xml.find("playingtime")['value'])
    game.minNumPlayers = int(xml.find("minplayers")['value'])
    game.maxNumPlayers = int(xml.find("maxplayers")['value'])
    return game
