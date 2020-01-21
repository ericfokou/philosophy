#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Ne pas se soucier de ces imports
import setpath
from bs4 import BeautifulSoup
from json import loads
from urllib.request import urlopen
from urllib.parse import urlencode, unquote, urldefrag
from pprint import pprint


# Si vous écrivez des fonctions en plus, faites-le ici


def getJSON(page):
    params = urlencode({
      'format': 'json',  # TODO: compléter ceci
      'action': 'parse',  # TODO: compléter ceci
      'prop': 'text',  # TODO: compléter ceci
      'redirects': 'true',
      'page': page})
    API = "https://fr.wikipedia.org/w/api.php"  # TODO: changer ceci
    response = urlopen(API + "?" + params)
    return response.read().decode('utf-8')


def getRawPage(page):
    parsed = loads(getJSON(page))
    # print(type(parsed), list(parsed.keys()))
    # print(list(parsed['parse'].keys()))
    # print(parsed['parse']['title'])
    # print(parsed['parse']['text']['*'][:5])
    try:
        title = parsed['parse']['title']  # TODO: remplacer ceci
        content = parsed['parse']['text']['*']  # TODO: remplacer ceci
        return title, content
    except KeyError:
        # La page demandée n'existe pas
        return None, None


def getPage(page):
    try:
        title, content = getRawPage(page)
        if (content == None):
            return title, None
        soup = BeautifulSoup(content,'html.parser')
        #print(soup.encode("utf-8"))
        #dd
        aList = []
        cpt = 0
        for p in soup.find_all('p', recursive=False):
            for a in p.find_all('a', href=True):
                aFormated = urldefrag(unquote(a['href'])).url.replace("_", " ")
                if (aFormated.startswith('/wiki/') and ":" not in aFormated and aFormated[6:] not in aList):
                    aList.append(aFormated[6:])
                    cpt = cpt + 1
                    if (cpt == 10):
                        return title,aList
        #print(len(aList))
        # aList = filter(lambda x: 'wiki' in x, aList)
        #aList = [lien[6:] for lien in aList if (lien.startswith('/wiki/') and ":" not in lien)] # question 5 lien rouge commence par /w/ et externe n'ont pas /wiki/
        #print(len(aList))
        return title,aList
    except (RuntimeError, TypeError, NameError):
        # La page demandée n'existe pas
        return None, []


if __name__ == '__main__':
    # Ce code est exécuté lorsque l'on exécute le fichier
    print("Ça fonctionne !")
    
     # Voici des idées pour tester vos fonctions :
    # pprint(getJSON("Philosophie"))
    #pprint(getPage("Philosophique"))
    #pprint(getPage("Philosophique"))
    #pprint(getPage("Utilisateur:A3nm/INF344"))
    print(getPage("Geoffrey Miller"))