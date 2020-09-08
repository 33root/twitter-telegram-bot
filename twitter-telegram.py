import time
import telepot
import tweepy
import logging 
import config
from IPython import embed
from socket import error as SocketError
import errno


def telegram_alert(tweet, bot):
    try:
        bot.sendMessage(config.group_id, tweet.text)
    except SocketError as e:
        if e.errno != errno.ECONNRESET:
            raise
        pass
    logging.info("PUBLICADO     " + tweet.text)

def setup():
    token = config.token
    bot = telepot.Bot(token)
    logging.info(bot.getMe())
    return bot

if __name__ == "__main__":
    try:
        logging.basicConfig(filename='telegram-twitter-bot.log', level=logging.INFO)
        bot = setup()
        auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
        auth.set_access_token(config.access_token, config.access_token_secret)
        api = tweepy.API(auth)
        tweets = api.user_timeline(config.user) #trae los ultimos 20 tweets
        ref_tweet = tweets[0]
        logging.info("Ref tweet text: "  + ref_tweet.text)
        logging.info("Ref tweet id: " + str(ref_tweet.id))

        while 1:
            time.sleep(config.sleep)
            tweets = api.user_timeline(config.user)
            last_tweet = tweets[0]
            if ref_tweet != last_tweet:
                telegram_alert(last_tweet, bot)
                ref_tweet = last_tweet
            pass
    except Exception as e:
        logging.error(str(e))