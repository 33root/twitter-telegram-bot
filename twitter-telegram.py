import time
import telepot
import tweepy
import logging 
import config
import urllib3, requests
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
    try:
        bot = telepot.Bot(token)
        logging.info(bot.getMe())
        return bot
    except requests.exceptions.ReadTimeout as e:
        logging.error("Read Time Out in Telepot")
        time.sleep(30)
        setup()

def main(): 
        logging.basicConfig(filename='telegram-twitter-bot.log', level=logging.INFO)
        auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
        auth.set_access_token(config.access_token, config.access_token_secret)
        api = tweepy.API(auth)
        tweets = api.user_timeline(config.user) #trae los ultimos 20 tweets
        ref_tweet = tweets[0]
        logging.info("Ref tweet text: "  + ref_tweet.text)
        logging.info("Ref tweet id: " + str(ref_tweet.id))
        while 1:
            time.sleep(config.sleep)
            tweets = []
            try: 
                tweets = api.user_timeline(config.user)
                last_tweet = tweets[0]
                embed()
                if ref_tweet != last_tweet:
                    bot = setup()
                    telegram_alert(last_tweet, bot)
                    ref_tweet = last_tweet

            except tweepy.error.TweepError as e:
                logging.info("ConnectionError in while")
                continue
            except urllib3.exceptions.ProtocolError as e:
                logging.error("Protocol Error")
                continue
    

if __name__ == "__main__":
    try:
        main()

    except tweepy.error.TweepError as e:
        logging.info("ConnectionError in  ")
        time.sleep(60)
        main()
    except Exception as e:
        embed()
        logging.error(str(e))