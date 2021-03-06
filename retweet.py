#!/usr/bin/env python3
# coding: utf8
"""This script checks tweets of defined users for defined hashtags in random order.
When a suitable tweet is found, which wasn't previously retweeted, it gets retweeted"""

import random
import time
from twython import TwythonError

import api_setup

while True:
    with open('data/users') as user_list:
        users = user_list.read().splitlines()

    while True:
        try:
            if users:
                selected = users[random.randint(0, len(users))-1]
                users.remove(selected)

                try:
                    timeline = api_setup.api.get_user_timeline(
                        screen_name=selected,
                        count=1,
                        exclude_replies='true',
                        include_rts='true')
                except TwythonError as e:
                    print(e)

                for tweet in timeline:
                    nId = tweet['id_str']

                    with open('data/buzzwords') as buzzword_list:
                        buzzwords = buzzword_list.read().splitlines()

                    if any(n in tweet['text'] for n in buzzwords):

                        if nId not in open('data/retweet-blacklist').read():
                            print('Tweeted: ' + tweet['text'])
                            with open('data/retweet-blacklist', 'a') as blacklist:
                                blacklist.write('\n' + nId)

                            api_setup.api.retweet(id=nId)
                            time.sleep(900)
                        else:
                            time.sleep(2)
                            break
                    else:
                        time.sleep(2)
                        break
            else:
                time.sleep(5)
                break
        except TwythonError as e:
            print(e)
