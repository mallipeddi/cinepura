"""
>>> from BeautifulSoup import BeautifulSoup
>>> import urllib2
>>> page = urllib2.urlopen("http://sg.movies.yahoo.com/Showtimes/movies/")
>>> soup = BeautifulSoup(page)
>>> movie_tables = soup.findAll("table", {"class":"mv_st"})
>>> for movie in movie_tables:
...   print movie.findNext('h1').a.string
...   for cinema in movie.findAll("tr", {"class":"st_n"}):
...     for c in cinema.findAll("td"):
...       if c.h3:
...         print "\t%s @ %s" % (c.h3.a.string, c.contents[-1])
Be Kind Rewind
	Filmgarde Leisure Park Kallang @  11:10AM  1:10PM  5:10PM 

	SHAW Lido Theatre @  12:50PM  5:15PM  7:30PM  9:45PM 

	SHAW Balestier @   1:00PM  5:00PM 

Becoming Jane
	Cathay The Cathay Cineplex @  11:30AM  2:00PM  4:30PM  7:00PM  9:25PM 

	Cathay Orchard @  12:20AM  2:45AM 12:25PM  2:45PM  5:05PM  7:30PM  9:55PM 
"""

from django.shortcuts import render_to_response, get_object_or_404
from django.http import *
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.core.cache import cache

import datetime, random, os, math
from django.conf import settings

def home(request):
    movies = simplejson.load(open(os.path.join(settings.APP_DIR, 'data/daily.txt'), "r"))
    movies.sort(key = lambda x: x['rating'], reverse=True)
    print len(movies)
    return render_to_response("iphone/home.html", {'movies':movies}, context_instance=RequestContext(request))