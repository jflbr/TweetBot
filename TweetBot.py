# -*- coding: utf-8 -*-
#!/usr/local/bin/python2.7


from tweepy.auth import OAuthHandler
from tweepy.streaming import StreamListener, Stream
from TweetBotConfig import TweetBotConfig

import tweepy, time


class AuthenticationError(Exception):
    pass

class TweetBot(StreamListener):
    ''' TweetBot cls '''
    def __init__(self,cfgFile="config",*args,**kwargs):

        StreamListener.__init__(self,*args,**kwargs)

        self.cfg   = TweetBotConfig(cfgFile=kwargs.get('cfgFile',cfgFile))

        self.api   = None
        self.auths = None

        self.setupAuthentication()


    def setupAuthentication(self):
        self.auths = OAuthHandler(self.cfg.consumer_key, self.cfg.consumer_key_secret)
        self.auths.set_access_token(self.cfg.access_token, self.cfg.access_token_secret)
        self.api = tweepy.API(self.auths)
        try:
            print 'Verifying bot credentials..........',
            self.api.verify_credentials()
            print 'OK\n\n'
        except Exception as e:
            print 'FAILED'
            print(e)
            raise AuthenticationError()



    def on_data(self, raw_data):
        ''' Implementation of StreamListener.on_data method '''
        try:
            screen_name = raw_data.lower().split('"screen_name":"')[1].split('","location"')[0].replace(",", "")
            tweet_sid   = raw_data.split('"id":')[1].split('"id_str":')[0].replace(",", "")
            retweet_ed  = raw_data.lower().split('"retweeted":')[1].split(',"possibly_sensitive"')[0].replace(",", "")
            tweet_text  = raw_data.lower().split('"text":"')[1].split('","source":"')[0].replace(",", "")


            # Exit if the bot is the tweet owner
            if screen_name.lower() == self.api.me().screen_name.lower():
                return

            print '+ Tweet from {} :\n\t{}\n\n'.format(screen_name,tweet_text)

            if not any(a_acc.lower() == screen_name.lower() for a_acc in self.cfg.whitelist_accounts):
                if not any(acc.lower() == screen_name.lower() for acc in self.cfg.banned_accounts):
                    if not any(a_wrds.lower() in screen_name.lower() for a_wrds in self.cfg.whitelist_words):
                        if not any(word.lower() in tweet_text.lower() for word in self.cfg.banned_words):
                            if("false" in retweet_ed):

                                # Retweet if allowed
                                if self.cfg.strategy['retweet']:
                                    self.retweet(tweet_sid)
                                    time.sleep(2)

                                # Fav if allowed
                                if self.cfg.strategy['fav']:
                                    self.fav(tweet_sid)

                                # Follow if allowed
                                #if self.cfg.strategy['follow']:
                                    # if api.exists_friendship(api.me().id, screen_name.lower()):
                                    #     print 'I already follow @{}'.format(screen_name.lower())
                                    # else:
                                    #     print 'Trying to follow @{}'.format(screen_name.lower())
                                    #     self.followUsers([screen_name.lower()])

                                    # if screen_name.lower() != self.api.me().screen_name.lower():
                                    #     print 'Trying to follow @{}'.format(screen_name.lower())
                                    #     self.followUsers([screen_name.lower()])
                            else:
                                pass
                        else:
                            print 'Banned word in {}\nSkipping...'.format(tweet_text)
                    else:
                        pass
                else:
                    print 'Banned account @{}\nSkipping...'.format(screen_name)
            return True
        except Exception as e:
            print(str(e))


    def on_error(self, status_code):
        ''' Implementation of StreamListener.on_error method '''
        try:
            print( "error " + status_code)
        except Exception as e:
            print(" ++ wuuuut? ++ " + str(e))

    def retweet(self,tweet_sid):
        try:
            self.api.retweet(tweet_sid)
        except Exception as e:
            if e.code == 327: pass
            else: print( "\terror {} - {}\n".format(e['code'],e['message']))
            print( "\terror {} - {}\n".format(e['code'],e['message']))


    def fav(self,tweet_sid):
        try:
            self.api.create_favorite(tweet_sid)
        except Exception as e:
            print(str(e))

    def tweetPost(self,tweet_text):
        try:
            self.api.update_status(status=tweet_text)
        except Exception as e:
            print(str(e))

    def getUserFollowers(self,user):
        pass

    def followUsers(self,users):
        for user in users:
            self.api.create_friendship(user)
            print "Followed {}".format(user)
            time.sleep(2)

    def unfollowUsers(self,users):
        for user in users:
            self.api.destroy_friendship(user)
            print "Unfollowed {}".format(user)

    def unfollowFollowers(self):
        users = self.api.friends_ids()
        self.unfollowUsers(users)



def main():
    bot = TweetBot(cfgFile="config-dev")

    try:
        twt = Stream(bot.auths, bot)
        twt.filter(track=bot.cfg.track_words) # OR (follow = bot.cfg.follow_accounts)
    except Exception as e:
        print(str(e))
        pass


if __name__ == '__main__':
    main()
