from collections import defaultdict
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class inverted_index(object):
    """
    get posting
    """

    def __init__(self, path, uselessTerm):
        self.path = path
        self.uselessTerm = uselessTerm
        self.postings = defaultdict(list)

    def tweet_tokenize(self, line):
        line = line.lower()
        a = line.index("username")
        b = line.index("clusterno")
        c = line.rindex("tweetid") - 1
        d = line.rindex("errorcode")
        e = line.index("text")
        f = line.index("timestr") - 3
        line = line[c:d] + line[a:b] + line[e:f]  # tweet_id + username + text

        terms = word_tokenize(line)
        print('terms:', terms)
        result = []
        for word in terms:
            expected_str = ''
            if expected_str not in self.uselessTerm:
                result.append(expected_str)
        return result

    def get_postings(self, document):
        file = open(self.path)
        lines = file.readlines()
        for line in lines:
            line = self.tweet_tokenize(line)
            tweet_id = line[0]
            line.pop(0)
            unique_terms = set(line)
            for term in unique_terms:
                if term in self.postings.keys():
                    self.postings[term].append(tweet_id)
                else:
                    self.postings[term] = tweet_id
