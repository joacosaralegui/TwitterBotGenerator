# TwitterBotGenerator

Using RASA and the Twitter API, you can generate a bot simulating a user.

## Chatbot
Inside the chatbot folder you can find the Rasa project (version 1.10.0) that uses tweets info to generate a chatbot.
The dataset to train the chatbot can be automatically generated using <b>dataset.py</b> file. <br/><br/>
<b>IMPORTANT!</b> Google universal-sentence-encoder_4 is required, be sure to download it.


## Twitter
Get a Twitter developer account for your bot account and load the credentials in <b>credentials.py.temp</b>, then rename the file to <b>credentials.py</b>
