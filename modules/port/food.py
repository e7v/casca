#1/usr/bin/env/python
"""
food.py - Jenni Food Module
by afuhrtrumpet

More info:
 * casca: https://github.com/myano/casca/
 * Casca: http://github.com/e7v/casca/
"""

from yelpapi import YelpAPI
import random


def food(casca, input):
    if not hasattr(casca.config, 'yelp_api_credentials'):
        return
    yelp_api = YelpAPI(casca.config.yelp_api_credentials['consumer_key'], casca.config.yelp_api_credentials['consumer_secret'], casca.config.yelp_api_credentials['token'], casca.config.yelp_api_credentials['token_secret'])

    location = input.group(2)

    if not location:
        casca.say("Please enter a location.")
        return

    done = False
    max_offset = 5

    try:
        while not done:
            offset = random.randint(0, max_offset)
            response = yelp_api.search_query(category_filter="restaurants", location=location, limit=20, offset=offset)
            if len(response['businesses']) > 0:
                done = True
                casca.say("How about, " + response['businesses'][random.randint(0, len(response['businesses']) - 1)]['name'] + "?")
            else:
                max_offset = offset - 1
    except YelpAPI.YelpAPIError:
        casca.say("Invalid location!")

food.commands = ["food"]
food.priority = 'medium'
food.example = '.food <location>'

if __name__ == '__main__':
    print __doc__.strip()
