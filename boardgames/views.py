from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django import http
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe
import json
import datetime
from json import JSONEncoder
from boardgames.models import Boardgame
from boardgames.models import GamePlay

def home(request):

  allGames = Boardgame.objects.all()

  gameJSONs = []
  for currGame in allGames:
    gameJSON = {}
    gameJSON["name"] = currGame.name
    gameJSON["rating"] = currGame.rating
    gameJSON["ranking"] = currGame.ranking
    gameJSON["minNumPlayers"] = currGame.minNumPlayers
    gameJSON["maxNumPlayers"] = currGame.maxNumPlayers
    gameJSON["playTime"] = currGame.playTime
    gameJSON["complexity"] = currGame.complexityWeight
    gameJSON["bggId"] = currGame.bggId
    gameJSON["bggUrl"] = currGame.bggUrl
    gameJSON["numRatings"] = currGame.numRatings

    gameJSONs.append(gameJSON)
  return render(request, 'home.html', {'allGames': mark_safe(json.dumps(gameJSONs, cls=DjangoJSONEncoder))})

def addGamePlay(request):
  # request.POST.getlist('aaa')
  data = json.loads(request.body);
  id = int(data["gameId"]);
  dateStr = str(data["date"]);
  playDate = datetime.datetime.strptime(dateStr, "%m/%d/%Y"); 
  play = GamePlay(bggId = id, date = playDate);
  play.save();
  return HttpResponse("Success");
