from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django import http
from django.template import RequestContext, loader
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe
from urllib.request import urlopen
import json
from json import JSONEncoder
from boardgames.models import HNStory
from boardgames.models import TopStoryIdsByTime
from boardgames.models import HNTopStory
import string

def home(request):
  topStories = HNTopStory.objects.all()
  storyJSONs = []
  for story in topStories:
    if story.marked_deleted is True:
      continue;
    jsonStory = json.loads(story.story);
    if not jsonStory.get('score'):
      story.delete();
      continue;
    jsonstory = json.loads(story.story);
    jsonstory['hnstoryid'] = story.hnStoryId;
    storyJSONs.append(jsonstory)
  # sort by score
  stories = sorted(storyJSONs, key=lambda st: int(st.get('score')), reverse=True);
  stories_w_top_urls = filter_stories_for_top_urls(stories)

  # remove top from original
  for story in stories_w_top_urls:
    stories.remove(story)

  stories = sorted(stories, key=lambda st: int(st.get('score')), reverse=True);
  stories_w_top_urls = sorted(stories_w_top_urls, key=lambda st: int(st.get('score')), reverse=True);
  context = {
               'allStories': mark_safe(json.dumps(stories, cls=DjangoJSONEncoder)),
               'top_urls': mark_safe(json.dumps(stories_w_top_urls, cls=DjangoJSONEncoder))
            }
  return render(request, 'topstories.html', context)

# Returns a list of stories that have a url in the top urls.
def filter_stories_for_top_urls(stories):
  urls = get_top_url_strings()
  filtered = []
  for story in stories:
    url = story.get('url')
    is_top = False
    for topurl in urls:
      if url and url.find(topurl) != -1:
        is_top = True
        break
    if is_top:
      filtered.append(story)
  return filtered

# Returns a list of sites that consider top ones.
# Stories with urls containing these will be put in a separate area.
def get_top_url_strings():
  urls = ["washingtonpost.com",
          "nytimes.com",
          "newyorker.com",
          "techcrunch.com",
          "greatist.com",
          "neal.is",
          "randsinrepose.com",
          "arstechnica.com",
          "lifehacker.com",
          "kickstarter.com",
          "npr.org",
          "bbc.com",
          "sfgate.com",
          "economist.com",
          "jasonshen.com",
          "rickyyean.com",
          "mercurynews.com"
         ];
  return urls;

def update_top_items(request):
    url = 'https://hacker-news.firebaseio.com/v0/topstories.json';
    data = json.load(urlopen(url));
    jsonStr = json.dumps(data);
    topIdsObj = TopStoryIdsByTime(storyIds = data);
    topIdsObj.save();
    return http.HttpResponse("updated");

# removes top stories from the db.
def remove_top_items(request):
    ids = request.POST.getlist('storyId');
    allTopStories = HNTopStory.objects.all();
    delCount = 0;
    for story in allTopStories:
        storyId = story.hnStoryId
        if str(storyId) in ids or storyId in ids:
            story.marked_deleted = True
            story.save()
            delCount = delCount + 1;
    return redirect("/topStories");

