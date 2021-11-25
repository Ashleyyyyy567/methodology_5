import json
import pandas as pd
from urllib.parse import urlparse
from urlextract import URLExtract

def url_checking(): 
    # initialize variables
    users = dict()
    url_count = 0
    retweet_count = 0
    total_count = 0
    misinfo_count = 0
    fact_count = 0
    none_count = 0
    multiple_url_cout = 0

    df = pd.read_csv("test/testdata/misinformation_source.csv")
    df = df[df['Domain'].notna()]
    misinfo = list(df.Domain)
    # fact checker website comes from https://library.csi.cuny.edu/c.php?g=619342&p=4310783
    fact_checker = ['politifact.com', 'factcheck.org', 'washingtonpost.com', 'snopes.com', 'reporterslab.org', 'factcheck.org', 
                   'flackcheck.org', 'mediabiasfactcheck.com', 'npr.org']


    with open('test/testdata/tweet_output.jsonl', 'r') as f:
        for line in f:
            tweet = json.loads(line)
            total_count += 1
            url_binary = int("https://" in tweet['text'])
            url_count += url_binary
            if url_binary == 1: 
                extractor = URLExtract()
                urls = extractor.find_urls(tweet['text'])

                if len(urls) > 1: 
                    multiple_url_cout += 1

                for url in urls: 
                    o = urlparse(url)
                    base_url = o.netloc
                    if base_url in misinfo: 
                        misinfo_count += 1
                    elif base_url in fact_checker: 
                        fact_count += 1
                    else: 
                        none_count += 1


            retweet = int(tweet['text'].startswith("rt @"))
            retweet_count += retweet

            user = tweet['user_name']
            if (user not in users.keys()): 
                users[user] = 1
            else: 
                users[user] += 1



    unique_user = len(users.keys())
    tweet_per_user = users.values()
    
    print("number of url contains in the tweet")
    print(url_count)
    print("number of retweets")
    print(retweet_count)
    print("total number of tweets")
    print(total_count)
    print("number of url contains misinformation")
    print(misinfo_count)
    print("number of url contains fact checking")
    print(fact_count)
    print("number of url contains neural url")
    print(none_count)
    print("number of tweet contains multiple urls")
    print(multiple_url_cout)
    print("unique user")
    print(unique_user)
    
    return users

def top100(): 
    tweets_dict = dict()
    retweets_dict = dict()
    min_retweet = 1000000
    min_id = 0

    with open('test/testdata/tweet_output.jsonl', 'r') as f:
        count = 0
        for line in f:
            tweet = json.loads(line)
            if count < 100: 
                tweets_dict[tweet['user_name']] = tweet['text']
                retweets_dict[tweet['user_name']] = int(tweet['retweet'])
                if int(tweet['retweet']) < min_retweet: 
                    min_retweet = int(tweet['retweet'])
                    min_id = tweet['user_name']
                    count += 1
            else: 
                if int(tweet['retweet']) > min_retweet: 
                    del tweets_dict[min_id]
                    del retweets_dict[min_id]

                    tweets_dict[tweet['user_name']] = tweet['text']
                    retweets_dict[tweet['user_name']] = int(tweet['retweet'])

                    min_retweet = min(pd.Series(retweets.values()))
                    idx = pd.Series(retweets.values()).idxmin()
                    min_id = pd.Series(retweets.keys())[idx]

    return tweets_dict

def top100_url_checking():
    tweets_dict = top100()
    url_count = 0
    misinfo_count = 0
    fact_count = 0

    df = pd.read_csv("test/testdata/misinformation_source.csv")
    df = df[df['Domain'].notna()]
    misinfo = list(df.Domain)
    # fact checker website comes from https://library.csi.cuny.edu/c.php?g=619342&p=4310783
    fact_checker = ['politifact.com', 'factcheck.org', 'washingtonpost.com', 'snopes.com', 'reporterslab.org', 'factcheck.org', 
                   'flackcheck.org', 'mediabiasfactcheck.com', 'npr.org']


    for value in list(tweets_dict.values()): 
        url_binary = int("https://" in value)
        url_count += url_binary
        if url_binary == 1: 
            extractor = URLExtract()
            urls = extractor.find_urls(value)

            for url in urls: 
                o = urlparse(url)
                base_url = o.netloc
                if base_url in misinfo: 
                    misinfo_count += 1
                elif base_url in fact_checker: 
                    fact_count += 1

    print('misinformation')
    print(misinfo_count / url_count)
    print('fact checking')
    print(fact_count / url_count)
    
if __name__ == '__main__':
    url_checking()
    top100_url_checking()
    
    
    
