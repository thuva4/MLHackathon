import json
import os

import requests

api_token = 'API_KEY'
api_url_base = 'http://api.yelp.com/v3/businesses/search?location={0}&limit=50&offset={1}&term={2}'

headers = {'Content-Type': 'application/json',
           'Authorization': 'Bearer {0}'.format(api_token)}


def get_review_info(location, search_term):
    responses = []
    for i in range(0, 950, 50):
        api_url = api_url_base.format(location, i, search_term)
        responseRaw = requests.get(api_url, headers=headers)
        response = json.loads(responseRaw.content.decode('utf-8'))
        print(response)
        if responseRaw.status_code == 200:
            if response['businesses'].__len__() == 0:
                break
            responses.append(response)
        else:
            return responses
    return responses

term = 'resrestaurant_name'
f = open("{}.txt".format(term), "a+")

with open('usaCities.json') as json_file:
    data = json.load(json_file)
    cities = []
    for location in data['cities']:
        if location['city'] not in cities:
            cities.append(location['city'])
    print(cities.__len__())
    for location in cities:
        base_urls = []
        review_info = get_review_info(location, term)
        if review_info is not None:
            print("Here's your info: ")
            for response in review_info:
                for business in response['businesses']:
                    if term in business['url'] and business['url'] not in base_urls:
                        base_urls.append(business['url'])
        else:
            print('[!] Request Failed')

        print(base_urls.__len__())
        for url in base_urls:
            f.write(url + "\n")
        print("Finished : {}".format(location))

f.close()
