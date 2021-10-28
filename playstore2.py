import pandas as pd
import json
import ssl
import play_scraper
from google_play_scraper import app, Sort, reviews_all
from tinydb import TinyDB
from time import sleep
import openpyxl
##proviamo a fixare sta roba con ssl
ssl._create_default_https_context = ssl._create_unverified_context

# le librerie sono: play-scraper, google-play-scraper, google-play-scraper-py, pandas, tinydb, openpyxl

#keywords_general_OLD = ['serious game', 'game', 'children', 'educational', 'learning', 'learn', 'educative', 'family', 'pedagogical']
#keywords_onetime_OLD = ['adhd', 'dyslexia', 'hyperactivity', 'autism', 'rehab', 'sen', 'specific learning needs',
#                    'dyscalculia', 'Behaviour Emotional Social Difficulty', 'mentally retarded',
#                    'down syndrome', 'disabled', 'disability', 'clinical']

keywords_general = ['serious game', 'game', 'children', 'educational', 'educative', 'pedagogical']
keywords_onetime = ['adhd', 'dyslexia', 'hyperactivity', 'autism', 'sen', 'specific learning needs',
                    'dyscalculia', 'Behaviour Emotional Social Difficulty', 'mentally retarded',
                    'down syndrome']

allowed_categories = ['EDUCATION', 'FAMILY', 'FAMILY_EDUCATION', 'GAME_EDUCATIONAL']
min_rating = 3.79
max_results_per_search = 35 #integer number; max number allowed is 50


# let's create the columns of the final database.
all_titles = []
all_url = []
all_rating = []
all_categories = []

# list that contains all the suitable games that we found using this script
all_games = []

def AddToDatabase(game_list, games_database):
    for games in game_list:
        url = games['url'].split('/store/apps/details?id=')
        url = url[1]
        goOn = True
        for g in games_database:
            if (g.url == url):
                print('duplicated: ' + url)
                goOn = False
        if (goOn):
            result = app(
                url,
                lang='en',  # defaults to 'en'
                country='us',  # defaults to 'us'
            )

            print(url)
            goon = False
            while (goon is False):
                details = ""
                try :
                     details = play_scraper.details(url)
                except:
                    sleep(0.5)
                if (len(details) > 5):
                    goon = True

            print(details['category'])
            category = details['category']
            if(allowed_categories.__contains__(category[0])):
                if(type(result['score']) is float):
                    if (type(result['contentRating']) is not None):
                        if (result['score'] >= min_rating):
                            if(result['contentRating'] == "Everyone"):
                                games_database.append(game(games['title'], url, result['score'], result['contentRating'], category))
                                all_titles.append(games['title'])
                                all_url.append(url)
                                all_rating.append(result['score'])
                                all_categories.append(category)
                                print("added " + url)
                            else:
                                print("not for everyone " + result['contentRating'] + " " + url)
                        else:
                            print("score too low " + str(result['score']) + " " + url)
                    else:
                        print("content rating missing " + url)
                else:
                    print("score not found " + url)
            else:
                print("not in the right category " + url)

    return games_database

# Non ho usato il database che ci hanno dato in classe, ho usato subito le librerie online
# Nonostante quello che dice nelle slide, non serve usare la libreria json per
# interfacciarsi con i risultati delle librerie del play store

# Solita classe che contiene le informazioni che ci interessano:

class game:
    title = ''
    url = ''
    rating = 0
    age_range = ''
    category = ''

    def __init__(self, titolo, url_, voto, eta, categoria):
        self.title = titolo
        self.url = url_
        self.rating = voto
        self.age_range = eta
        self.category = categoria




# uso la libreria play_scraper per cercare nell'intero database di google play quelli educativi (BISOGNA ESPANDERE STA
# RICERCA IN MANIERA SENSATA)

# write a code that combines all the words, and then search for all the results
for word in keywords_general:
    goon = False
    while (goon is False) :
        games_list=[]
        try :
            games_list = play_scraper.search(word)
        except :
            sleep (0.5)
        if (len(games_list) > 1):
            goon = True

    games_list = games_list[0:max_results_per_search]
    AddToDatabase(games_list, all_games)

print('\n')

for word in keywords_onetime:
    goon = False
    while (goon is False):
        games_list=[]
        try:
            games_list = play_scraper.search(word)
        except :
            sleep (0.5)
        if (len(games_list) > 1):
            goon = True
    games_list = games_list[0:max_results_per_search]
    AddToDatabase(games_list, all_games)
    for word2 in keywords_general:
        goon = False
        while (goon is False):
            parola = word + ' ' + word2
            try:
                games_list = play_scraper.search(parola)
            except :
                sleep (0.5)
            if (len(games_list) > 1):
                goon = True
        games_list = games_list[0:max_results_per_search]
        AddToDatabase(games_list, all_games)

print(len(all_games))

# Now we will use pandas to create the .csv final dataset
result = {'Titles': all_titles,
        'URL': all_url,
        'Category': all_categories,
        'Rating': all_rating }
print(result)
df = pd.DataFrame(result)
df.to_excel('Database_v2.xlsx')

