from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django import http
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe
import json
import datetime
from json import JSONEncoder
from boardgames.models import Meal
from boardgames.models import Other
from boardgames.models import RestaurantToTry 

def food(request):

  allMeals = Meal.objects.all()
  mealJSONs = []

  for m in allMeals:
    mealjson = {}
    mealjson["date"] = m.date.isoformat()
    mealjson["meal"] = m.meal
    mealjson["venue"] = m.venue
    mealjson["yelpUrl"] = m.yelpUrl
    mealjson["food"] = m.food
    mealjson["attendee"] = m.attendee
    mealJSONs.append(mealjson);

  allToTry = RestaurantToTry.objects.all()
  toTry = []
  for r in allToTry:
    rjson = {}
    rjson["yelpUrl"] = r.yelpUrl
    rjson["venue"] = r.venue
    rjson["notes"] = r.notes
    rjson["area"] = r.area
    rjson["food"] = r.food
    toTry.append(rjson)
    
  return render(request, 'home.html', {
    'allMeals': mark_safe(json.dumps(mealJSONs, cls=DjangoJSONEncoder)),
    'allToTry': mark_safe(json.dumps(toTry, cls=DjangoJSONEncoder))});
  
# Handler for adding a meal
def addMeal(request):
  dateStr = request.POST.get('date')
  mealType = request.POST.get('meal')
  venue = request.POST.get('venue')
  url = request.POST.get('url')
  food = request.POST.get('food')
  attendees = request.POST.get('who')
  mealDate = datetime.datetime.strptime(dateStr, "%m/%d/%Y"); 

  
  meal = Meal(date = mealDate, meal = mealType, venue = venue, yelpUrl = url, food = food, attendee = attendees)
  meal.save()
  return redirect('/');

#Handler for loading other data.
def other(request):
  allOther = Other.objects.all();
  otherjson = [];
  for o in allOther:
    ojson = {}
    ojson["date"] = o.date.isoformat()
    ojson["type"] = o.type;
    ojson["desc"] = o.desc;
    ojson["attendee"] = o.attendee
    otherjson.append(ojson)
  return render(request, 'other.html', {'allOther': mark_safe(json.dumps(otherjson, cls=DjangoJSONEncoder))});

# Handler for saving other data.
def addOther(request):
  dateStr = request.POST.get('date')
  typeStr = request.POST.get('type')
  desc = request.POST.get('desc')
  attendee = request.POST.get('attendee')
  oDate = datetime.datetime.strptime(dateStr, "%m/%d/%Y");
  o = Other(date = oDate, type = typeStr, desc = desc, attendee = attendee)
  o.save()
  return redirect('/other');  


# Handler for saving restaurants to try.
def addRestaurantToTry(request):

  venue = request.POST.get('venue')
  url = request.POST.get('url')
  foodType = request.POST.get('food')
  location = request.POST.get('area')
  notes = request.POST.get('notes')

  toTry = RestaurantToTry(yelpUrl = url, venue = venue, notes = notes, area = location, food = foodType)
  toTry.save()
  return redirect('/');


