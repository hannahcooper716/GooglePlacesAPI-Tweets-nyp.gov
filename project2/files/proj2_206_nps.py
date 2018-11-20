from bs4 import BeautifulSoup
import requests
import json
from requests_oauthlib import OAuth1
import secrets
## proj_nps.py
## Skeleton for Project 2, Winter 2018
## ~~~ modify this file, but don't rename it ~~~

CACHE_FNAME = 'cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}

def get_unique_key(url):
    return url

def make_request_using_cache(baseurl):
    unique_ident = get_unique_key(baseurl)

    if unique_ident in CACHE_DICTION:
      #print("Getting cached data...")
      return CACHE_DICTION[unique_ident]

    else:
        #print("Making a request for new data...")
    # Make the request and cache the new data
        resp = requests.get(baseurl) #delete params but deal with header
        CACHE_DICTION[unique_ident] = resp.text #get rid of json
        dumped_json_cache = json.dumps(CACHE_DICTION)
        f = open(CACHE_FNAME,"w")
        f.write(dumped_json_cache)
        f.close() # Close the open file
        return CACHE_DICTION[unique_ident]


try:
    nearby_cache = open('nearby_cache_file.json', 'r')
    contents = nearby_cache.read()
    diction = json.loads(contents)
    nearby_cache.close()

    # if there was no file, no worries. There will be soon!
except:
    diction = {}

# A helper function that accepts 2 parameters
# and returns a string that uniquely represents the request
# that could be made with this info (url + params)
def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)

# The main cache function: it will always return the result for this
# url+params combo. However, it will first look to see if we have already
# cached the result and, if so, return the result from cache.
# If we haven't cached the result, it will get a new one (and cache it)
def make_request_nearby(baseurl, params):
    unique_ident = params_unique_combination(baseurl,params)

    ## first, look in the cache to see if we already have this data
    if unique_ident in diction:
        #print("Getting cached data...")
        return diction[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        #print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(baseurl, params)
        diction[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(diction)
        fw = open('nearby_cache_file.json',"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return diction[unique_ident]


try:
    cache_twitter = open('twitter_cache.json', 'r')
    contents_twitter = cache_twitter.read()
    diction_twitter = json.loads(contents_twitter)
    cache_twitter.close()
except:
    diction_twitter = {}

def make_request_twitter_cache(baseurl, params, auth):
    indent_twitter = params_unique_combination(baseurl,params)

    ## first, look in the cache to see if we already have this data
    if indent_twitter in diction_twitter:
        #print("fetching cache data...")
        return diction_twitter[indent_twitter]
    else:
        #print("making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(baseurl, params, auth=auth)
        r = json.loads(resp.text)['statuses']
        diction_twitter[indent_twitter] = r
        dumped_json_cache = json.dumps(diction_twitter)
        fw = open('twitter_cache.json',"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return diction_twitter[indent_twitter]
## you can, and should add to and modify this class any way you see fit
## you can add attributes and modify the __init__ parameters,
##   as long as tests still pass
##
## the starter code is here just to make the tests run (and fail)
class NationalSite:
    def __init__(self, type = 'No Type', name = 'No Name', desc = 'No Desc', url=None, street = "No Street", city = "No City", state = "No State", zipcode = "No Zipcode"):
        self.type = type
        self.name = name
        self.description = desc
        self.url = url

        self.address_street = street
        self.address_city = city
        self.address_state = state
        self.address_zip = zipcode
    def __str__(self):
        return '{} ({}): {}, {}, {} {}'.format(self.name, self.type, self.address_street, self.address_city, self.address_state, self.address_zip)

## you can, and should add to and modify this class any way you see fit
## you can add attributes and modify the __init__ parameters,
##   as long as tests still pass
##
## the starter code is here just to make the tests run (and fail)
class NearbyPlace():
    def __init__(self, name = "no Name", lat = 'No Lat', long_ = "No Long"):
        self.name = name
        self.latitude = lat
        self.longitude = long_

    def __str__(self):
        return self.name

## you can, and should add to and modify this class any way you see fit
## you can add attributes and modify the __init__ parameters,
##   as long as tests still pass
##
## the starter code is here just to make the tests run (and fail)
class Tweet:
    def __init__(self, username = "no username", text = 'no text', creation_date = 'no date', num_retweets = 'no retweets', num_favorites = 'no favorites', popularity_score = 'no score', id_ = 'no id'):
        self.username = username
        self.text = text
        self.creation_date = creation_date
        self.num_retweets = num_retweets
        self.num_favorites = num_favorites
        self.popularity_score = popularity_score
        self.id = id_

    def __str__(self):
        return "@{}: {} \n [retweeted {} times] \n [favorited {} times] \n [popularity {}] \n [tweeted on {}] | [id: {}]".format(self.username, self.text, self.num_retweets, self.num_favorites, self.popularity_score, self.creation_date, self.id)



## Must return the list of NationalSites for the specified state
## param: the 2-letter state abbreviation, lowercase
##        (OK to make it work for uppercase too)
## returns: all of the NationalSites
##        (e.g., National Parks, National Heritage Sites, etc.) that are listed
##        for the state at nps.gov
def get_sites_for_state(state_abbr):
    baseurl = 'https://www.nps.gov/state/{}/index.htm'.format(state_abbr)
    html = make_request_using_cache(baseurl)
    soup = BeautifulSoup(html, 'html.parser')
    searching_div = soup.find_all(class_ = "col-md-9 col-sm-9 col-xs-12 table-cell list_left")
    base = 'https://www.nps.gov'
    #print(searching_div)
    list_of_parks = []
    for x in searching_div:
        type_of_park = x.find('h2').text
        #print(type_of_park)
        name_of_park = x.find('a').text
        #print(name_of_park)
        desc_of_park = x.find('p').text.strip()
        #print(desc_of_park)
        end_of_url = x.find('a')['href']
        #print(end_of_url)
        url = base + end_of_url
        #print(url)
        #all_park = NationalSite(type_of_park, name_of_park, desc_of_park, url)
        #print(all_park)


        html1 = make_request_using_cache(url)
        soup1 = BeautifulSoup(html1, 'html.parser')
        searching_div = soup1.find_all('p', class_ ="adr")
        #print(searching_div)
        if len(searching_div)==0:
            all_parks = NationalSite(type= type_of_park, name = name_of_park, desc = desc_of_park, url = url)
            list_of_parks.append(all_parks)
        for x in searching_div:
            try:
                street = x.find('span', itemprop = 'streetAddress', class_ = 'street-address').text.strip()
            except:
                street = 'No Street'
             #print(street)
            try:
                city = x.find('span', itemprop = 'addressLocality').text.strip()
            except:
                city = 'No City'
             #print(city)
            try:
                state = x.find('span', itemprop = 'addressRegion').text.strip()
            except:
                state = 'No State'
             #print(state)
            try:
                zipcode = x.find('span', itemprop = 'postalCode', class_ = 'postal-code').text.strip()
            except:
                zipcode = 'No Zipcode'
             #print(zipcode)
             # print(list_of_parks)
            all_parks = NationalSite(type= type_of_park, name = name_of_park, desc = desc_of_park, url = url, street = street, city = city, state = state, zipcode = zipcode)
             #print(all_parks.__str__())
            list_of_parks.append(all_parks)
    return list_of_parks
    #print(list_of_parks)

#print(get_sites_for_state('mi'))


## Must return the list of NearbyPlaces for the specified NationalSite
## param: a NationalSite object
## returns: a list of NearbyPlaces within 10km of the given site
##          if the site is not found by a Google Places search, this should
##          return an empty list
def get_nearby_places_for_site(site_object):
    name = site_object.name
    type_= site_object.type
    combo = name + " "+ type_
    google_places_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'
    data_text = make_request_nearby(google_places_url, params = {'key': secrets.google_places_key, 'query': combo})
    results = data_text["results"]
    if len(results)== 0:
        return []
    lat = results[0]['geometry']['location']['lat']
    long_ = results[0]['geometry']['location']['lng']
    coordinates = str(lat) + "," + str(long_)

    nearby_places = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
    text_data = make_request_nearby(nearby_places, params = {'key': secrets.google_places_key, 'location': coordinates, 'radius': 10000})
    nearby_places = []
    results_nearby = text_data["results"]
    if len(results_nearby) == 0:
        return []
    for x in results_nearby:
        lat = x['geometry']['location']['lat']
        long_ = x['geometry']['location']['lng']
        name = x['name']
        nearby_instance = NearbyPlace(name, lat, long_)
        nearby_places.append(nearby_instance)
    return nearby_places
#instance = NationalSite('national park', "Yellow Stone", 'beautiful', 'url')
#print(get_nearby_places_for_site(instance))

## Must return the list of Tweets that mention the specified NationalSite
## param: a NationalSite object
## returns: a list of up to 10 Tweets, in descending order of "popularity"
def get_tweets_for_site(site_object):
    consumer_key = secrets.twitter_api_key
    consumer_secret = secrets.twitter_api_secret
    access_token = secrets.twitter_access_token
    access_secret = secrets.twitter_access_token_secret
    url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
    auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
    requests.get(url, auth=auth)

    twitter_link = 'https://api.twitter.com/1.1/search/tweets.json?'
    name = site_object.name
    type_ = site_object.type
    full_name = str(name) + ',' + str(type_)
    twitter_data = make_request_twitter_cache(twitter_link, {'Name': name,'q': full_name, 'count': 100}, auth)
    #print(twitter_data)
    original_tweets = []
    if len(twitter_data) == 0:
        return []
    number = 0
    for x in twitter_data:
        if 'RT' in x['text'].split()[0]:
            continue
        else:
            number = number + 1
            if number > 10:
                break
            text = x['text']
            #print(text)
            username = x['user']['screen_name']
            #print(username)
            creation_date = x['created_at']
            #print(creation_date)
            num_retweets = x['retweet_count']
            #print(num_retweets)
            num_favorites = x['favorite_count']
            #print(num_favorites)
            popularity_score = (num_retweets*2) + (num_favorites*3)
            #print(popularity_score)
            id_ = x['id']
            #print(id_)
            tweets = Tweet(username = username, text = text, creation_date = creation_date, num_retweets = num_retweets, num_favorites = num_favorites, popularity_score = popularity_score, id_ = id_)
            #print(tweets)
            original_tweets.append(tweets)

    sorted_tweets = sorted(original_tweets, key= lambda x: x.popularity_score, reverse=True)
    for x in sorted_tweets:
        #print(x.__str__())
        return sorted_tweets
# site2 = get_sites_for_state('il')
# print(get_tweets_for_site(site2[0]))

# instance = NationalSite(type ='national park', name ="Yellow Stone", desc= 'beautiful', url='url')
# instance1 = NationalSite(type = 'national park', name = "isle royale", desc = 'beautiful', url = 'url')
# get_tweets_for_site(instance1)

if __name__ == "__main__":
    resp = input('Enter command (or “help” for options): ')
    while resp != "exit":
        number = 0
        # places = google_places_url(resp)
        # nearby_places_ = nearby_places(resp)
        # tweets_ = twitter_link(resp)
        # while resp == "list" or "nearby" or "tweets":
            # imp = split[1]
        if "list" in resp:
            abbreviations = {
                'Alabama': 'AL',
                'Alaska': 'AK',
                'Arizona': 'AZ',
                'Arkansas': 'AR',
                'California': 'CA',
                'Colorado': 'CO',
                'Connecticut': 'CT',
                'Delaware': 'DE',
                'Florida': 'FL',
                'Georgia': 'GA',
                'Hawaii': 'HI',
                'Idaho': 'ID',
                'Illinois': 'IL',
                'Indiana': 'IN',
                'Iowa': 'IA',
                'Kansas': 'KS',
                'Kentucky': 'KY',
                'Louisiana': 'LA',
                'Maine': 'ME',
                'Maryland': 'MD',
                'Massachusetts': 'MA',
                'Michigan': 'MI',
                'Minnesota': 'MN',
                'Mississippi': 'MS',
                'Missouri': 'MO',
                'Montana': 'MT',
                'Nebraska': 'NE',
                'Nevada': 'NV',
                'New Hampshire': 'NH',
                'New Jersey': 'NJ',
                'New Mexico': 'NM',
                'New York': 'NY',
                'North Carolina': 'NC',
                'North Dakota': 'ND',
                'Ohio': 'OH',
                'Oklahoma': 'OK',
                'Oregon': 'OR',
                'Pennsylvania': 'PA',
                'Rhode Island': 'RI',
                'South Carolina': 'SC',
                'South Dakota': 'SD',
                'Tennessee': 'TN',
                'Texas': 'TX',
                'Utah': 'UT',
                'Vermont': 'VT',
                'Virginia': 'VA',
                'Washington': 'WA',
                'West Virginia': 'WV',
                'Wisconsin': 'WI',
                'Wyoming': 'WY'}
            list_ = {}
            split = resp.split()
            for x in abbreviations:
                if abbreviations[x] == split[1].upper():
                    state = x
            print('National Sites in ' + state)
            places__ = get_sites_for_state(split[1])
            for x in places__:
                number = number + 1
                list_[x] = number
                print(str(number) + " " + x.__str__())
        elif "nearby" in resp:
            nearby = {}
            split = resp.split()
            # imp = split[1]
            # for x in list_:
            #     if imp == list_[x]:
            #         imp = x
            #         near_places = get_nearby_places_for_site(x)
            #         print(near_places)
            for y in list_:
                if int(split[1]) == list_[y]:
                    near_places = get_nearby_places_for_site(y)
            if len(near_places) == 0:
                print('Unable to find places nearby.')
                resp = input("Please enter a new command (or 'help' for options): ")
                if 'exit' == resp:
                    print("Bye!")
                    exit()
                continue
            for x in near_places:
                number = number + 1
                nearby[x] = number
                print(str(number) + " " + x.__str__())

        #make sure I have correct key-value pairs and am getting the data from the correct place
        #made a function for incorrect inputs
        elif "tweets" in resp:
            split = resp.split()
            for x in list_:
                if int(split[1]) == list_[x]:
                    top_tweets = get_tweets_for_site(x)
            if len(top_tweets) == 0:
                print('Unable to find tweets for this place.')
                resp = input("Please enter a new command (or 'help' for options): ")
                if 'exit' == resp:
                    print("Bye!")
                    exit()
                continue
            for x in top_tweets:
                print(x.__str__())
        elif resp == 'help':
            print ('list <stateabbr> \n\t available anytime \n\t lists all National Sites in a state \n\t valid inputs: a two-letter state abbreviation')
            print('nearby <results_number> \n\t available only if there is an active result set \n\t lists all Places nearby a given result \n\t valid inputs: an integer 1-len(result_set_size)')
            print('tweets <result_number> \n\t available only if there is an active results set \n\t lists u to 10 most "popular" tweets that mention the selected Site')
            print('exit \n\t exits the program')
            print('help \n\t lists available commands (these instructions)')
        else:
            resp = input("Not a valid Command. Please enter a new command (or 'help' for options): ")
            if 'exit' == resp:
                print("Bye!")
                break
            continue
        resp = input('Enter command (or “help” for options): ')
        if 'exit' == resp:
            print('Bye!')
            break
