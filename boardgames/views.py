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
  allPlays = GamePlay.objects.all()

  gameJSONs = []
  for currGame in allGames:
    gameJSON = {}
    gameJSON["name"] = currGame.name
    gameJSON["lowername"] = currGame.name.lower()
    gameJSON["rating"] = currGame.rating
    gameJSON["ranking"] = currGame.ranking
    gameJSON["minNumPlayers"] = currGame.minNumPlayers
    gameJSON["maxNumPlayers"] = currGame.maxNumPlayers
    gameJSON["playTime"] = currGame.playTime
    gameJSON["complexity"] = currGame.complexityWeight
    gameJSON["bggId"] = currGame.bggId
    gameJSON["bggUrl"] = currGame.bggUrl
    gameJSON["numRatings"] = currGame.numRatings

    plays = filter_plays_for_game(allPlays, currGame.bggId)

    # sort plays by date
    plays = sorted(plays, key=lambda gp: gp.date.toordinal(), reverse=True);
    gameJSON["numPlays"] = len(plays)

    if len(plays) > 0:
      gameJSON["lastPlayed"] = plays[0].date.isoformat()
    if len(plays) > 1:
      gameJSON["firstPlayed"] = plays[-1].date.isoformat()
    gameJSONs.append(gameJSON)

  byDate = form_json_plays_by_day(allPlays)
  return render(request, 'home.html', {'allGames': mark_safe(json.dumps(gameJSONs, cls=DjangoJSONEncoder)),
                                       'byDate': mark_safe(json.dumps(byDate, cls=DjangoJSONEncoder))})


# Returns a json object of all plays by day of week
def form_json_plays_by_day(allPlays) :
  byDate = {};
  for i in range(0, 8) :
    byDate[i] = [];
  
  for play in allPlays:
    obj = {};
    obj["date"] = play.date.isoformat()
    obj["bggId"] = play.bggId
    byDate[play.date.weekday()].append(obj)
  return byDate;


# Handler for adding a play of a particular game.
def addGamePlay(request):
  # request.POST.getlist('aaa')
  data = json.loads(request.body);
  id = int(data["gameId"]);
  dateStr = str(data["date"]);
  playDate = datetime.datetime.strptime(dateStr, "%m/%d/%Y");
  notesStr = str(data["notes"])
  play = GamePlay(bggId = id, date = playDate, notes = notesStr);
  play.save();
  return HttpResponse("Success");



# Returns list of plays for game with the given bggId.
def filter_plays_for_game(allPlays, id):
  plays = []
  for play in allPlays:
    if play.bggId == id:
      plays.append(play)

  return plays
