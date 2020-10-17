#!/usr/bin/env python
import tweepy
import chatbot_conection
import json

# Fetch credentials
from credentials import *

# Load api
api = create_api()

def create_api():
    print("** Connecting to Twitter API")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        print("Error creating API")
        raise e
    print("API created")
    return api

def clean_mentions(tweet):
    if 'user_mentions' in tweet.entities:
        for entity in tweet.entities['user_mentions']:
            tweet.full_text = tweet.full_text.replace("@"+entity['screen_name'],"") 

def clean_text(tweet):
    clean_mentions(tweet)
    tweet.full_text = tweet.full_text.strip().replace("\n",". ").replace("\"","'")

def get_tweets(user_id):
    # 200 tweets to be extracted 
    number_of_tweets = 3200
    tweets = []
    counter = 0
    for pages in tweepy.Cursor(api.user_timeline, id=user_id, count=200,tweet_mode="extended").pages():    
        if counter < number_of_tweets:
            tweets.extend(list(pages))
            counter += 200    
            
    return tweets 

def get_tweets_from_all(user_ids):
    tweets = []
    for user_id in user_ids:
        tweets.extend(get_tweets(user_id))
    return tweets

def get_replies(user_ids):
    # Fetch all tweets from every user
    tweets =  get_tweets_from_all(user_ids)
    print("Tweets: ",len(tweets))
    return [t for t in tweets if t.in_reply_to_status_id]

def get_pairs(user_ids):
    print("** Fetching all replies...")
    replies = get_replies(user_ids)
    pairs = []
    print("** Fetching tweets that were replied...")
    for i in range(0,len(replies),100):
        ids = {}
        for j in range(0,100):
            if i+j < len(replies):
                ids[replies[i+j].in_reply_to_status_id] = replies[i+j]
            else: 
                break
        
        tweets = api.statuses_lookup(list(ids.keys()),tweet_mode="extended")
        for tweet in tweets:
            tweet_reply = ids[tweet.id]
            # Cleanse mentions from tweet text and strip
            clean_text(tweet)            
            clean_text(tweet_reply)

            pairs.append((tweet,tweet_reply))
            
    return pairs

def retrieve_conversations(replies):
    # Fetch side b of replies
    conversations = {}
    for tweet in replies:
        # Fetch emssage that triggered the response tweet
        trigger = api.get_status(tweet.in_reply_to_status_id, tweet_mode="extended")

        # Cleanse mentions from tweet text and strip
        clean_text(trigger)
        clean_text(tweet)

        # Add to conversations
        conversations[tweet.id] = [(trigger,tweet)]
    return conversations
    
def join_if_thread(conversations):
    conversations_items = list(conversations.values())
    for items in conversations_items:
        root = items[0]
        tweet = root[1]
        trigger = root[0]
        if trigger.in_reply_to_status_id in conversations:
            conversations[trigger.in_reply_to_status_id].extend(items)
            del conversations[tweet.id]

def get_conversations(user_ids):
    
    # Fetch the ones that are replies to other tweets
    replies = get_replies(user_ids)
    
    # Get all the tweets which this replies reply to
    conversations = retrieve_conversations(replies)
    
    # Join conversations if correspond to a thred
    join_if_thread(conversations)

    return conversations

def check_mentions(since_id):
    print("Retrieving mentions")
    new_since_id = since_id

    mentions = tweepy.Cursor(
        api.mentions_timeline,
        since_id=since_id,
        tweet_mode="extended"
    ).items()

    for tweet in mentions:
        print(f"Answering to {tweet.user.name}")
        new_since_id = max(tweet.id, new_since_id)
        response = chatbot_conection.get_response(tweet)

        if response:
            api.update_status(
                status = response,
                in_reply_to_status_id = tweet.id,
                auto_populate_reply_metadata=True
            )

    return new_since_id


if __name__=="__main__":
    # TODO: load this var from file
    with open('state.json', 'r') as fp:
        since_id = json.load(fp)

    since_id = check_mentions(since_id)

    with open('state.json', 'w') as fp:
        json.dump(since_id, fp)

