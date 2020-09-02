import time
import telepot
import tweepy
import logging 
import config


def telegram_alert(tweet, bot):
    text = tweet.text + " " + tweet.entities['urls'][0]['url']
    bot.sendMessage( tweet.text + " " + tweet.entities['urls'][0]['url'])
    logging.info("PUBLICADO     " + text)

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
            sleep(config.sleep)
            tweets = api.user_timeline(config.user)
            if ref_tweet != tweets[0]:
                telegram_alert(tweets[0], bot)
                ref_tweet = tweets[0]
            pass
    except Exception as e:
        logging.error(str(e))