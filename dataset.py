#!/usr/bin/env python
import twitter
import tensorflow_hub as hub
import numpy as np
from rasa_objects import *
import os

print("** Loading module...")
module_url = "data/universal-sentence-encoder_4" 
model = hub.load(module_url)
print ("** Module %s loaded" % module_url)

def embed(input):
    return model(input)

def build_dataset(conversations, username):
    responses = []
    intents = []
    stories = []
    
    for intent, response in conversations:
        intents.append(intent)
        responses.append(response)
        stories.append({'_id': "story_"+ str(hash(intent)) + str(hash(response)),'story':[{'intent':intent._id,'response':response._id}]})

    # create array of tweet information: username,  
    # tweet id, date/time, text 
    if not os.path.exists(f'data/{username}'):
        os.makedirs(f'data/{username}')

    with open(f'data/{username}/nlu.md', mode='w') as open_file:
        open_file.writelines(i.nlu_declaration() for i in intents)
    
    with open(f'data/{username}/domain.yml', mode='w') as open_file:
        open_file.write("intents:\n")
        open_file.writelines(i.domain_declaration() for i in intents)
        open_file.write("\nresponses:\n")
        open_file.writelines(i.domain_declaration() for i in responses)
        open_file.write('session_config:\n  session_expiration_time: 60\n  carry_over_slots_to_new_session: true')

    with open(f'data/{username}/stories.md', mode='w') as open_file:
        for story in stories:
            open_file.write("## %s\n" % story['_id'])
            open_file.writelines("* %s\n  - %s\n" % (s['intent'],s['response']) for s in story['story'])
            open_file.write("\n")


def create_dataset(user_ids):
    # TODO: CLEANUP THIS FUNCTION
    grouping = False
    pairs = twitter.get_pairs(user_ids)
    
    tweets = []
    replies = []
    for tweet,reply in pairs:
        tweets.append(tweet.full_text)
        replies.append(reply.full_text)

    print("** Creating embeddings...")
    tweets_result = embed(tweets)
    print("** Calculating similarity...")
    similarity_matrix = np.inner(tweets_result, tweets_result)
    
    sims = []
    if grouping:
        for i in range(len(tweets)-1):
            for j in range(i+1,len(tweets)):
                if similarity_matrix[i][j] > 0.8:
                    intent1,response1 = Intent([tweets[i]]),Response([replies[i]])
                    intent2,response2 = Intent([tweets[j]]),Response([replies[j]])
                    sims.append((
                        (intent1,response1),
                        (intent2,response2)
                    ))

        result = []
        
        for tup in sims:
            for idx, already in enumerate(result):
                # check if any items are equal
                if any(item in already for item in tup):
                    # tuples are immutable so we need to set the result item directly
                    result[idx] = already + tuple(item for item in tup if item not in already)
                    break
            else:
                # else in for-loops are executed only if the loop wasn't terminated by break
                result.append(tup)

        conversations = []
        for items in result:
            intent = items[0][0]
            response = items[0][1]

            for item in items:
                intent = RasaObject.join(intent, item[0], Intent)
                response = RasaObject.join(response, item[1], Response)
            conversations.append((intent,response))
    else:
        conversations = []
        for i in range(min(len(tweets),200)):
            intent,response = Intent([tweets[i]]),Response([replies[i]])
            conversations.append((intent,response))

    # SIMS = [ (A, B), (A, C) ]
    # Build dataset given the conversations
    build_dataset(conversations,user_ids[0])

def main():    
    create_dataset(["andresmalamud"])

if __name__ == "__main__":
    main()