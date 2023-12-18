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
  notes = models.TextField(null = True)

#
class HNStory(models.Model):
  storyJSON = models.TextField()
  hnUserId = models.IntegerField()
  hnStoryId = models.IntegerField(unique = True, primary_key = True)

# object for storing the list of top HN story ids as of a given time.
class TopStoryIdsByTime(models.Model):
  storyIds = models.TextField()
  topTime = models.DateTimeField(auto_now = True, unique = True, primary_key = True)

# Object for storing a top story from HN.
class HNTopStory(models.Model):
  hnStoryId = models.IntegerField(unique = True, primary_key = True)
  date = models.DateField(auto_now = True)
  story = models.TextField()
  marked_deleted = models.BooleanField(default = False)
