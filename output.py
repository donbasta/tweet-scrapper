from time import strftime, localtime
from datetime import datetime, timezone
from utils import utc_to_local, Tweet_formats
import format


def _get_mentions(tw):
    try:
        mentions = [
            {
                'screen_name': _mention['screen_name'],
                'name': _mention['name'],
                'id': _mention['id_str'],
            } for _mention in tw['entities']['user_mentions']
            if tw['display_text_range'][0] < _mention['indices'][0]
        ]
    except KeyError:
        mentions = []
    return mentions


def _get_reply_to(tw):
    try:
        reply_to = [
            {
                'screen_name': _mention['screen_name'],
                'name': _mention['name'],
                'id': _mention['id_str'],
            } for _mention in tw['entities']['user_mentions']
            if tw['display_text_range'][0] > _mention['indices'][1]
        ]
    except KeyError:
        reply_to = []
    return


def getText(tw):
    """Replace some text
    """
    text = tw['full_text']
    text = text.replace("http", " http")
    text = text.replace("pic.twitter", " pic.twitter")
    text = text.replace("\n", " ")

    return text


class tweet:
    type = "tweet"

    def __init__(self):
        pass


def Tweet(tw, config):
    t = tweet()
    t.id = int(tw['id_str'])
    t.id_str = tw["id_str"]
    t.conversation_id = tw["conversation_id_str"]

    # parsing date to user-friendly format
    _dt = tw['created_at']
    _dt = datetime.strptime(_dt, '%a %b %d %H:%M:%S %z %Y')
    _dt = utc_to_local(_dt)
    t.datetime = str(_dt.strftime(Tweet_formats['datetime']))
    # date is of the format year,
    t.datestamp = _dt.strftime(Tweet_formats['datestamp'])
    t.timestamp = _dt.strftime(Tweet_formats['timestamp'])
    t.user_id = int(tw["user_id_str"])
    t.user_id_str = tw["user_id_str"]
    t.username = tw["user_data"]['screen_name']
    t.name = tw["user_data"]['name']
    t.place = tw['geo'] if 'geo' in tw and tw['geo'] else ""
    t.timezone = strftime("%z", localtime())
    t.mentions = _get_mentions(tw)
    t.reply_to = _get_reply_to(tw)
    try:
        t.urls = [_url['expanded_url'] for _url in tw['entities']['urls']]
    except KeyError:
        t.urls = []
    try:
        t.photos = [_img['media_url_https'] for _img in tw['entities']['media'] if _img['type'] == 'photo' and
                    _img['expanded_url'].find('/photo/') != -1]
    except KeyError:
        t.photos = []
    try:
        t.video = 1 if len(tw['extended_entities']['media']) else 0
    except KeyError:
        t.video = 0
    try:
        t.thumbnail = tw['extended_entities']['media'][0]['media_url_https']
    except KeyError:
        t.thumbnail = ''
    t.tweet = getText(tw)
    t.lang = tw['lang']
    try:
        t.hashtags = [hashtag['text']
                      for hashtag in tw['entities']['hashtags']]
    except KeyError:
        t.hashtags = []
    try:
        t.cashtags = [cashtag['text'] for cashtag in tw['entities']['symbols']]
    except KeyError:
        t.cashtags = []
    t.replies_count = tw['reply_count']
    t.retweets_count = tw['retweet_count']
    t.likes_count = tw['favorite_count']
    t.link = f"https://twitter.com/{t.username}/status/{t.id}"
    try:
        if 'user_rt_id' in tw['retweet_data']:
            t.retweet = True
            t.retweet_id = tw['retweet_data']['retweet_id']
            t.retweet_date = tw['retweet_data']['retweet_date']
            t.user_rt = tw['retweet_data']['user_rt']
            t.user_rt_id = tw['retweet_data']['user_rt_id']
    except KeyError:
        t.retweet = False
        t.retweet_id = ''
        t.retweet_date = ''
        t.user_rt = ''
        t.user_rt_id = ''
    try:
        t.quote_url = tw['quoted_status_permalink']['expanded'] if tw['is_quote_status'] else ''
    except KeyError:
        t.quote_url = 0
    return t


def _output(output):
    try:
        print(output.replace('\n', ' '))
    except UnicodeEncodeError:
        print("unicode error [x] output._output")


async def checkData(tweet, config):
    tweet = Tweet(tweet, config)
    if not tweet.datestamp:
        print("[x] Hidden tweet found, account suspended due to violation of TOS")
        return

    output = format.Tweet(tweet)
    _output(output)


async def Tweets(tweets, config):
    await checkData(tweets, config)
