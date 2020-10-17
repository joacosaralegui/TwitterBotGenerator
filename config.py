# tweepy-bots/bots/config.py
import tweepy
import logging
import os
from credentials import *

logger = logging.getLogger()

def create_api():
    print("** Connecting to Twitter API")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api

"""
API key:



copy-light
API key secret:



copy-light
Bearer token:

AAAAAAAAAAAAAAAAAAAAAJtXHwEAAAAAkkmy8BooVO%2BIh6TWELpwj6D%2FUCo%3DX6DsjCWB70NswEYudEPa0PVRMCLXG8JGZ2jFY3SHTzrI6ib28c

Access token:



copy-light
Access token secret:


"""