from django.core.management.base import BaseCommand, CommandError
from django.core.serializers.json import DjangoJSONEncoder
from urllib.request import urlopen
import datetime
import json
import time
from boardgames.models import Boardgame
from bs4 import BeautifulSoup

# Command to fetch game list from boardgame geek
class Command(BaseCommand):
  def handle(self, *args, **options):
    print("Running load games")
    # only run few times a month, not daily
    currDay = datetime.datetime.now().day
    #if currDay != 25 and currDay != 10 and currDay != 14:
    #  return;
    maxNumPages = 40;
    baseUrl = "https://www.boardgamegeek.com/browse/boardgame/page/"
    allGames = Boardgame.objects.all();

    for i in range(1, maxNumPages):
      url = baseUrl + str(i)
      print("url: " + url);
      resp = urlopen(url)
      print("after open url")
      html = BeautifulSoup(resp.read(), 'html.parser')
      print("after html")
      try:
        table = html.find("table", id="collectionitems")
        print("after html table")
        rows = table.findAll("tr")

        print("Fetched table trs")
        rnum = 0
        # go thru each row in the table - each row representing a different game
        for currRow in rows:
          rnum += 1
          if rnum <= 2:
            print(f"ROW FOUND: {currRow}")
          tdElems = currRow.find_all("td", attrs={"class": "collection_rank"});
          print("here2")
          if len(tdElems) < 1:
            continue;
          print("here3")
          nameTd = currRow.find_all("td", attrs={"class": "collection_objectname"})[0]; 
          nameA = nameTd.find("a");
          name = nameA.contents[0]
          
          rank = str(tdElems[0].text.strip());
          print(f"here4:{rank}:{name}:{nameTd}:{nameA}")

          gameUrl = nameA['href'];

          # extract bgg id
          bggId = gameUrl[11:]
          bggId = bggId[0:bggId.find("/")]
          print("here5")
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
