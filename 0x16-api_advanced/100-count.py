#!/on to recursively GET the count of the specified words occuring
in the titles of the hot posts from a give subreddit"""
from requests import get


def count_words(subreddit, word_list, word_counts={}, after=None):
    """Recursively GET all the count of words from `word_list` occurring
    in the hot posts of `subreddit`"""
    word_list = list(set(word_list))
    r = get("https://www.reddit.com/r/{}/hot.json".format(subreddit),
            params={"raw_json": 1,
                    "g": "GLOBAL",
                    "after": after,
                    "limit": 100},
            headers={"User-Agent": "Andrew from Holberton"},
            allow_redirects=False)
    try:
        r.raise_for_status()
    except:
        pass
    else:
        try:
            for word in word_list:
                word_counts.setdefault(word, 0)
            children = r.json().get('data').get('children')
            for c in children:
                for word in word_list:
                    word_counts[word] += sum(map(lambda w: w == word.lower(),
                                                 c.get('data')
                                                 .get('title')
                                                 .lower()
                                                 .split()))
            after = r.json().get('data').get('after')
            if after is None:
                if all(map(lambda w: w[1] == 0, word_counts.items())):
                    print()
                else:
                    for word, count in sorted(word_counts.items(),
                                              key=lambda i: i[1],
                                              reverse=True):
                        if count > 0:
                            print("{}: {}".format(word, count))
            else:
                return count_words(subreddit, word_list,
                                   word_counts=word_counts, after=after)
        except:
            passiin/python3
"""Function to count words in all hot posts of a given Reddit subreddit."""
import requests


def count_words(subreddit, word_list, instances={}, after="", count=0):
    """Prints counts of given words found in hot posts of a given subreddit.

    Args:
        subreddit (str): The subreddit to search.
        word_list (list): The list of words to search for in post titles.
        instances (obj): Key/value pairs of words/counts.
        after (str): The parameter for the next page of the API results.
        count (int): The parameter of results matched thus far.
    """
    url = "https://www.reddit.com/r/{}/hot/.json".format(subreddit)
    headers = {
        "User-Agent": "linux:0x16.api.advanced:v1.0.0 (by /u/bdov_)"
    }
    params = {
        "after": after,
        "count": count,
        "limit": 100
    }
    response = requests.get(url, headers=headers, params=params,
                            allow_redirects=False)
    try:
        results = response.json()
        if response.status_code == 404:
            raise Exception
    except Exception:
        print("")
        return

    results = results.get("data")
    after = results.get("after")
    count += results.get("dist")
    for c in results.get("children"):
        title = c.get("data").get("title").lower().split()
        for word in word_list:
            if word.lower() in title:
                times = len([t for t in title if t == word.lower()])
                if instances.get(word) is None:
                    instances[word] = times
                else:
                    instances[word] += times

    if after is None:
        if len(instances) == 0:
            print("")
            return
        instances = sorted(instances.items(), key=lambda kv: (-kv[1], kv[0]))
        [print("{}: {}".format(k, v)) for k, v in instances]
    else:
        count_words(subreddit, word_list, instances, after, count)
