import numpy as np
from math import *


def process_data(file):
    """
    - Output Format: 
        - relevant_gain_dict:
            - {query_id:{tweet_id: gain, tweet_id: gain, ...}}
            - all relevant docs which gain > 0 for query
        - retrival_dict:
            - {query_id:[tweet_id, tweet_id, ...]}
            - retrieved docs according to query
    """
    relevant_gain_dict, retrival_dict = {}, {}

    with open(file, 'r') as f:
        for line in f:
            info = line.strip().split(' ')

            if info[0] not in relevant_gain_dict:  # info[0]=query_id
                relevant_gain_dict[info[0]] = {}
            if info[0] not in retrival_dict:
                retrival_dict[info[0]] = []

            retrival_dict[info[0]].append(info[2])  # info[2]=tweet_id

            if int(info[3]) > 0:  # info[3]=relevant
                relevant_gain_dict[info[0]][info[2]] = int(info[3])

    return relevant_gain_dict, retrival_dict


def MAP_eval(relevant_gain_dict, retrival_dict, k=100):
    '''Mean Average Precision'''
    APs = []
    for query in relevant_gain_dict.keys():
        retrival_list = retrival_dict[query]
        if len(retrival_list) <= 0:
            print('query[', query, '] has no docs retrived.')
            return []

        truth = set(relevant_gain_dict[query].keys())
        precision = []
        i = 0
        correct_num = 0
        for doc in retrival_list:
            i += 1
            if doc in truth:
                correct_num += 1
                precision.append(correct_num / i)

        if precision:
            ap = np.sum(precision) / len(truth)
            APs.append(ap)
        else:
            APs.append(0)

    return np.mean(APs)


def MRR_eval(relevant_gain_dict, retrival_dict, k=100):
    '''Mean Reciprocal Rank'''
    RRs = []
    for query in relevant_gain_dict.keys():
        retrival_list = retrival_dict[query]
        if len(retrival_list) <= 0:
            print('query[', query, '] has no docs retrived.')
            return []

        truth = set(relevant_gain_dict[query].keys())
        res = []
        i = 0
        for doc in retrival_list:
            i += 1
            if doc in truth:
                res.append(1 / i)
                break

        if res:
            rr = np.sum(res) / 1.0
            RRs.append(rr)
        else:
            RRs.append(0)

    return np.mean(RRs)


def NDCG_eval(relevant_gain_dict, retrival_dict, k=100):
    '''Normalized Discounted Cumulative Gain'''
    NDCGs = []
    for query in relevant_gain_dict.keys():
        retrival_list = retrival_dict[query]
        if len(retrival_list) <= 0:
            print('query[', query, '] has no docs retrived.')
            return []

        truth_gain = sorted(list(relevant_gain_dict[query].values()), reverse=True)
        i = 1
        dcg, idcg = 0.0, 0.0
        for doc in retrival_list[1:len(truth_gain)]: # 从第一个开始
            i += 1
            rel = relevant_gain_dict[query].get(doc, 0)
            dcg += rel / log(i, 2)
            idcg += truth_gain[i - 2] / log(i, 2)

        rel_1 = relevant_gain_dict[query].get(retrival_list[0], 0)
        dcg += rel_1
        ndcg = dcg / idcg
        NDCGs.append(ndcg)

    return np.mean(NDCGs)