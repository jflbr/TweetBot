#!/usr/local/bin/python2.7

import os, ConfigParser, inspect, hashlib, json


class TweetBotConfig(object):
    ''' TweetBotConfig cls '''

    def __init__(self,cfgFile='config'):
        # Bool initializer
        str_to_bool = lambda x : x.strip()=='True'
        
        path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

        # read config file
        self.config = ConfigParser.SafeConfigParser()
        self.config.read(os.path.join(path, "config"))

        self.consumer_key        = self.config.get("twitter","consumer_key")
        self.consumer_key_secret = self.config.get("twitter","consumer_secret")
        self.access_token        = self.config.get("twitter","access_token")
        self.access_token_secret = self.config.get("twitter","access_token_secret")

        # Bot strategy on incoming data (tweets)
        self.strategy            = {'retweet':None,'fav':None,'follow':None}
        self.strategy['retweet'] = str_to_bool(self.config.get("strategy","retweet"))
        self.strategy['fav']     = str_to_bool(self.config.get("strategy","fav"))
        self.strategy['follow']  = str_to_bool(self.config.get("strategy","follow"))

        # Banned
        self.banned_accounts = json.loads(self.config.get("banned","accounts"))
        self.banned_words    = json.loads(self.config.get("banned","words"))

        # Tracked
        self.track_words     = json.loads(self.config.get("track","words"))

        # Follow accounts
        self.follow_accounts = json.loads(self.config.get("follow","accounts"))

        # Whitelist
        self.whitelist_accounts = json.loads(self.config.get("whitelist","accounts"))
        self.whitelist_words = json.loads(self.config.get("whitelist","words"))
