import requests
import ast
import functools
import pickle
import random


URL = "https://en.wikipedia.org/w/api.php"
S = requests.Session()
allLocations = {}

def saveData(DATA):
    pages = DATA['query']['pages']
    placesToLink = []
    for pageid in pages:
        page = pages[pageid]
        if 'coordinates' in page:
            coordinates = str(page['coordinates'][0]['lat']) + ',' + str(page['coordinates'][0]['lon'])
            placesToLink.append(page)
            if(random.random()<1):
                print(page['title'])
                print(coordinates)
            done = False
            links = []
            plcontinue = '||'
            while not done:
                PARAMS = {
                    "action": "query",
                    "format": "json",
                    "pageids": pageid,
                    "prop": "links",
                    "pllimit": 500,
                    "plnamespace": 0,
                    "plcontinue": plcontinue}
                R = S.get(url=URL, params=PARAMS)
                linkDATA = R.json()
                if 'continue' in linkDATA:
                    plcontinue = linkDATA['continue']['plcontinue']
                else:
                    done=True
                links += [link['title'] for link in linkDATA['query']['pages'][pageid]['links']]
            finalDataEntry = {'links': links, 'id': pageid, 'coordinates': coordinates}
            global allLocations
            allLocations[page['title']] = finalDataEntry

def loop():
    currentIndex = 1
    while True:
        pageIds = functools.reduce(lambda x, y: str(x)+'|'+str(y), range(currentIndex+50)[-49:], str(currentIndex))
        PARAMS = {
            "action": "query",
            "format": "json",
            "pageids": pageIds,
            "prop": 'coordinates',}
        R = S.get(url=URL, params=PARAMS)
        DATA = R.json()
        saveData(DATA)
        currentIndex += 50
        if currentIndex>1000000:
            return
def cleanLinks(locations):
    for pageName in locations:
        links = locations[pageName]['links']
        newLinks = []
        for link in links:
            if link in locations:
                newLinks.append(link)
        locations[pageName]['links'] = newLinks
    return locations


loop()
with open('bigData.pickle', 'wb') as handle:
    pickle.dump(allLocations, handle)
with open('bigData.pickle', 'rb') as handle:
    data = pickle.load(handle)
print('litttt')
cleanLinks(data)
print(data)
