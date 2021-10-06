import math
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


def cal_similarity(postings, query):
    term_num = defaultdict(int)  # 词数
    score_tid = defaultdict(list)


def get_postings(path):
    postings = defaultdict(dict)  # {term:{docID: log(tf)}}
    doc_nums = 0  # 文档数
    tf_per_doc = defaultdict(float)

    uselessTerm = ['username', 'tweetid', 'text']
    file = open(path)
    lines = file.readlines()
    for line in lines:
        doc_nums += 1
        line = tweet_tokenize(line, uselessTerm)
        tweet_id = line[0]
        line.pop(0)
        for term in line:  # 无需去重
            if term in tf_per_doc.keys():
                tf_per_doc[term] += 1
            else:
                tf_per_doc[term] = 1
        for term in line:
            tf_per_doc[term] = math.log(tf_per_doc[term]) + 1

        # 归一化
        nor = 0
        for term in tf_per_doc.keys():
            nor += tf_per_doc[term]
        nor = 1.0 / math.sqrt(nor)
        for term in tf_per_doc.keys():
            tf_per_doc[term] *= nor

        unique_term = set(line)
        for term in unique_term:
            if term in postings.keys():
                postings[term][tweet_id] += tf_per_doc[term]
            else:
                postings[term][tweet_id] = tf_per_doc[term]
    return postings, doc_nums


def search(postings, query):
    terms = query_tokenize(query)
    if not terms:
        exit(0)
