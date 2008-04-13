#!/usr/bin/env python
# encoding: utf-8
"""
daily.py

Created by Harish Mallipeddi on 2008-04-05.
Copyright (c) 2008 Harish Mallipeddi. All rights reserved.
"""

# --- SETTINGS ---
YAHOO_MOVIES_SINGAPORE = "http://sg.movies.yahoo.com/Showtimes/movies/"

# ----------------


from BeautifulSoup import BeautifulSoup
import urllib2
from django.utils import simplejson
import imdb

def fetch_yahoo_movies():
    print "Fetching movies list from Yahoo! Movies Singapore..."
    page = urllib2.urlopen(YAHOO_MOVIES_SINGAPORE)
    soup = BeautifulSoup(page)
    movie_tables = soup.findAll("table", {"class":"mv_st"})
    movies = []
    for table in movie_tables:
        movie = {}
        movie['title'] = table.findNext('h1').a.string
        movie['cinemas'] = []
        for cinema_tr in table.findAll("tr", {"class":"st_n"}):
            for c_td in cinema_tr.findAll("td"):
                if c_td.h3:
                    movie['cinemas'].append({
                            'name':c_td.h3.a.string,
                            'showtimes':c_td.contents[-1].replace("\n", ""),
                    })
        movies.append(movie)
    print "Done. Fetched %d movies." % len(movies)
    return movies

def fetch_imdb_info(ymovies):
    #ymovies = ymovies[:5]
    print "Fetching movie info from IMDB..."
    imdb_client = imdb.IMDb()
    for ymovie in ymovies:
        imdb_results = imdb_client.search_movie(ymovie['title'])
        if(imdb_results):
            imovie = imdb_results[0] # pick the first result from IMDB; this is the most likely match!
            print "\tFetching movie info for %s" % ymovie['title']
            imdb_client.update(imovie)
            ymovie['rating'] = imovie.get('rating', 0.0)
            ymovie['votes'] = imovie.get('votes', 0)
            ymovie['year'] = imovie.get('year', "")
            ymovie['languages'] = imovie.get('languages', [])
            ymovie['title'] = imovie.get('title', ymovie['title'])
            ymovie['cover_url'] = imovie.get('cover url', "")
            ymovie['directors'] = []
            for director in imovie.get('director', []):
                ymovie['directors'].append(director['name'])
            ymovie['genres'] = imovie.get('genre', [])
            ymovie['plot_outline'] = imovie.get('plot outline', "")
            for cert in imovie.get('certificates', ["Singapore:"]):
                country, letter_grade = cert.split(":")[:2]
                if country == u"Singapore":
                    ymovie['cert'] = letter_grade
            if len(imovie.get('cast', [])) > 5:
                imovie['cast'] = imovie['cast'][:5]
            ymovie['cast'] = []
            for person in imovie['cast']:
                ymovie['cast'].append(person['name'])
            print "\tDone."
        else:
            print "\tCannot find %s in IMDB." % ymovie['title']
    print "Done."
    return ymovies



def main():
    ymovies = fetch_yahoo_movies()
    imovies = fetch_imdb_info(ymovies)
    print "Writing data to file..."
    f = open("data/daily.txt", "w")
    f.write(simplejson.dumps(imovies))
    f.close()
    print "Done."

if __name__ == '__main__':
    main()
