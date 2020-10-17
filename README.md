# TwitterBotGenerator

Using RASA and the Twitter API, you can generate automatically a twitter bot that replicates an existing user.
Please request permission from the account you want to replicate and don't use this code for malicious purpouses.

## Chatbot
Inside the chatbot folder you can find the Rasa project (version 1.10.0) that uses tweets info to generate a chatbot.
The dataset to train the chatbot can be automatically generated using `python dataset.py` file in the <b>src</b> folder. The generated data and config files will be stored in <b>src/data</b> and you will have to move the manually to where they correspond. <br/><br/>

<b>IMPORTANT!</b> Google universal-sentence-encoder_4 is required, be sure to download it.


## Twitter
1. Create a new account for your bot.
2. Request a Twitter developer account for that account and load the credentials in <b>credentials.py.temp</b>, then rename the file to <b>credentials.py</b>
3. Run `python twitter.py` as a cron task every 5 to 10 minutes in order for the bot to respond. 
