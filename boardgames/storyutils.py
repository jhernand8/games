from urllib.request import urlopen
import json

def get_max_item_id():
    maxItemUrl = 'https://hacker-news.firebaseio.com/v0/maxitem.json'
    maxItemData = json.load(urlopen(maxItemUrl))
    return long(maxItemData);

# requests the item with the given id, return the json object.
def get_item(item_id):
    url = 'https://hacker-news.firebaseio.com/v0/item/' + str(item_id) + '.json'
    return json.load(urlopen(url))

def is_story(item_json):
    return "story" == item_json.get('type')

def is_deleted(item_json):
    return True == item_json.get('deleted')

# Returns the top items json.
def get_top_items():
  url = 'https://hacker-news.firebaseio.com/v0/topstories.json';
  data = json.load(urlopen(url));
  return data


