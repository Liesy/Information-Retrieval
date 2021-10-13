from functools import reduce
from math import *
from collections import defaultdict
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

wnl = WordNetLemmatizer()
tokenizer = RegexpTokenizer(r'\w+')

doc_nums = 0  # 文档数

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


def cal_similarity(postings, query):
    tf_query = {}  # 词数
    score_tweetid = {}

    for term in query:
        if term in tf_query.keys():
            tf_query[term] += 1.0
        else:
            tf_query[term] = 1.0

    for term in tf_query.keys():
        if term in postings.keys():
            doc_fre = len(postings[term])
        else:
            doc_fre = globals()['doc_nums']
        tf_query[term] = (log(tf_query[term]) + 1.0) * log(globals()['doc_nums'] / doc_fre)

    for term in query:
        if term in postings.keys():
            for tid in postings[term].keys():
                if tid in score_tweetid.keys():
                    score_tweetid[tid] += postings[term][tid] * tf_query[term]
                else:
                    score_tweetid[tid] = postings[term][tid] * tf_query[term]

    similarity = sorted(score_tweetid.items(), key=lambda x: x[1], reverse=True)
    return similarity


def get_postings(path):
    postings = defaultdict(dict)  # {term:{docID: log(tf)}}

    uselessTerm = ['username', 'tweetid', 'text']
    file = open(path)
    lines = file.readlines()
    for line in lines:
        globals()['doc_nums'] += 1
        line = tweet_tokenize(line, uselessTerm)
        tweet_id = line[0]
        line.pop(0)
        tf_per_doc = {}
        for term in line:  # 无需去重
            if term in tf_per_doc.keys():
                tf_per_doc[term] += 1.0
            else:
                tf_per_doc[term] = 1.0
        for term in line:
            tf_per_doc[term] = log(tf_per_doc[term]) + 1.0

        # 归一化
        nor = 0.0
        for term in tf_per_doc.keys():
            nor += tf_per_doc[term]
        nor = 1.0 / sqrt(nor)
        for term in tf_per_doc.keys():
            tf_per_doc[term] *= nor

        unique_term = set(line)
        for term in unique_term:
            postings[term][tweet_id] = tf_per_doc[term]
    return postings


def search_relevant_tweetid(postings, query):
    unique_query = set(query)
    sets = [set(postings[term].keys()) for term in unique_query]
    return reduce(set.union, [s for s in sets])


def search(postings, query):
    terms = query_tokenize(query)
    if not terms:
        exit(0)
    
    relevant_tweetids = search_relevant_tweetid(postings, terms)

    if not relevant_tweetids:
        print('no tweets matched any query terms for [%s]' % query)
        return

    print(str(len(relevant_tweetids)) + 'relevant tweet(s) totally...')
    print('---[top 50] score: tweet id---')

    scores = cal_similarity(postings, terms)
    i = 1
    for id, score in scores:
        if i > 50:
            break
        print('[no.%d] %f: %s' % (i, score, id))
        i += 1

    print('finished')
