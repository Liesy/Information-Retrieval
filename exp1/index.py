from collections import defaultdict
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

wnl = WordNetLemmatizer()
tokenizer = RegexpTokenizer(r'\w+')


def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


def tweet_tokenize(line, uselessTerm):
    line = line.lower()
    a = line.index('username')
    b = line.index('clusterno')
    c = line.rindex('tweetid') - 1
    d = line.rindex('errorcode')
    e = line.index('text')
    f = line.index('timestr') - 3
    line = line[c:d] + line[a:b] + line[e:f]  # tweet_id + username + text

    terms = tokenizer.tokenize(line)
    term_tag = pos_tag(terms)
    result = []
    for tag in term_tag:
        wordnet_pos = get_wordnet_pos(tag[1]) or wordnet.NOUN
        expected_str = wnl.lemmatize(tag[0], pos=wordnet_pos)
        if expected_str not in uselessTerm:
            result.append(expected_str)
    return result


def query_tokenize(query):
    query = query.lower()
    terms = tokenizer.tokenize(query)
    term_tag = pos_tag(terms)
    result = []
    for tag in term_tag:
        wordnet_pos = get_wordnet_pos(tag[1]) or wordnet.NOUN
        expected_str = wnl.lemmatize(tag[0], pos=wordnet_pos)
        result.append(expected_str)
    return result


def get_postings(path):
    postings = defaultdict(list)
    uselessTerm = ['username', 'tweetid', 'text']
    file = open(path)
    lines = file.readlines()
    for line in lines:
        line = tweet_tokenize(line, uselessTerm)
        tweet_id = line[0]
        line.pop(0)
        unique_terms = set(line)
        for term in unique_terms:
            if term in postings.keys():
                postings[term].append(tweet_id)
            else:
                postings[term] = [tweet_id]
    return postings


def option_and(postings, term1, term2):
    result = []
    if term1 not in postings or term2 not in postings:
        return result
    else:
        i, j = len(postings[term1]), len(postings[term2])
        x, y = 0, 0
        while x < i and y < j:
            if postings[term1][x] == postings[term2][y]:
                result.append(postings[term1][x])
                x += 1
                y += 1
            elif postings[term1][x] < postings[term2][y]:
                x += 1
            else:
                y += 1
    return result


def option_or(postings, term1, term2):
    result = []
    if term1 not in postings and term2 not in postings:
        return result
    elif term1 not in postings:
        result = postings[term2]
    elif term2 not in postings:
        result = postings[term1]
    else:
        result = postings[term1]
        for term in postings[term2]:
            if term not in postings[term1]:
                result.append(term)
    return result


def option_not(postings, term1, term2):
    result = []
    if term1 not in postings:
        return result
    elif term2 not in postings:
        result = postings[term1]
    else:
        for term in postings[term1]:
            if term not in postings[term2]:
                result.append(term)
    return result


def rankSearch(postings, terms):  # 倒排索引
    result = defaultdict(int)
    for item in terms:
        if item in postings:
            for tweetid in postings[item]:
                if tweetid in result:
                    result[tweetid] += 1
                else:
                    result[tweetid] = 1
    result = sorted(result.items(), key=lambda asd: asd[1], reverse=True)
    return result


def search(postings, query):
    terms = query_tokenize(query)
    if not terms:
        exit(0)
    if len(terms) == 3:
        if terms[1] == 'and':
            answer = option_and(postings, terms[0], terms[2])
            print(answer)
        elif terms[1] == 'or':
            answer = option_or(postings, terms[0], terms[2])
            print(answer)
        elif terms[1] == 'not':
            answer = option_not(postings, terms[0], terms[2])
            print(answer)
        else:
            print('syntax error')
            # exit(0)
    else:
        length = len(terms)
        answer = rankSearch(postings, terms)
        print('[Rank_Score: Tweetid]')
        for (tweetid, score) in answer:
            print(str(score / length) + ': ' + tweetid)
