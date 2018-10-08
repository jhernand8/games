from django.db import models

# Object for a particular boardgame and its ratings/info from BGG.
class Boardgame(models.Model):
  name = models.TextField()
  rating = models.FloatField()
  ranking = models.IntegerField()
  minNumPlayers = models.IntegerField()
  maxNumPlayers = models.IntegerField()
  playTime = models.IntegerField()
  complexityWeight = models.FloatField()
  bggId = models.IntegerField(unique = True, primary_key = True)
  bggUrl = models.TextField()
  numRatings = models.IntegerField()


# Represents a particular time I played a boardgame.
class GamePlay(models.Model):
  bggId = models.IntegerField()
  date = models.DateField()
  
