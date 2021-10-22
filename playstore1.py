import pandas as pd
import json
import ssl
import play_scraper
from google_play_scraper import app, Sort, reviews_all
from tinydb import TinyDB
##proviamo a fixare sta roba con ssl
ssl._create_default_https_context = ssl._create_unverified_context

# le librerie sono: play-scraper, google-play-scraper, google-play-scraper-py, pandas, tinydb
allowed_categories = ['EDUCATION', 'FAMILY', 'FAMILY_EDUCATION', 'GAME_EDUCATIONAL', 'HEALTH_AND_FITNESS', 'PARENTING']

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

            details = play_scraper.details(url)
            print(details['category'])
            category = details['category']
            if(allowed_categories.__contains__(category[0])):
                if(type(result['score']) is float):
                    if (type(result['contentRating']) is not None):
                        if (result['score'] >= 4):
                            if(result['contentRating'] == "Everyone"):
                                games_database.append(game(games['title'], url, result['score'], result['contentRating'], category[0]))
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


# lista che contiene tutti i giochi trovati
all_games = []

# uso la libreria play_scraper per cercare nell'intero database di google play quelli educativi (BISOGNA ESPANDERE STA
# RICERCA IN MANIERA SENSATA)

#keywords_general = ['serious game']
keywords_general = ['serious game', 'game', 'children', 'educational', 'learning', 'learn', 'educative', 'family', 'pedagogical']
keywords_onetime = ['adhd', 'dyslexia', 'hyperactivity', 'autism', 'rehab', 'sen', 'specific learning needs',
                    'dyscalculia', 'Behaviour Emotional Social Difficulty', 'mentally retarded',
                    'down syndrome', 'disabled', 'disability', 'clinical', 'specific learning disorder']
#keywords_onetime = []
# write a code that combines all the words, and then search for all the results

for word in keywords_general:
    games_list = play_scraper.search(word, )
    # print(play_scraper.search(word))
    # this_game = games_list[0]
    # this_url = this_game['url'].split('/store/apps/details?id=')
    # print(play_scraper.similar(this_url[1]))
    # games_list.extend(play_scraper.similar(this_url[1]))
    # print(len(games_list))
    print(len(games_list))
    AddToDatabase(games_list, all_games)

print('\n')

for word in keywords_onetime:
    games_list = play_scraper.search(word)
    AddToDatabase(games_list, all_games)
    for word2 in keywords_general:
        parola = word + ' ' + word2
        games_list = play_scraper.search(parola)
        AddToDatabase(games_list, all_games)

print(len(all_games))

# Now use pandas to manage your dataset
# Possible ready-to-use alternatives is to use access, sql, mongoDB
# We will use TinyDB, a document oriented database. It uses a simple

#db = TinyDB('./lab04DB.json')
