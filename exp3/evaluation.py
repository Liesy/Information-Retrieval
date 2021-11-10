import math
import numpy as np


def process_data(file):
    """
    - Output Format: 
        - tweetid_gain: {query_id:{tweet_id: gain, tweet_id: gain, ...}}
        - results: {query_id:[tweet_id, tweet_id, ...]}
    """
    gain_dict, res_dict = {}, {}

    with open(file, 'r') as f:
        for line in f:
            info = line.strip().split(' ')

            if info[0] not in gain_dict:  # info[0]=query_id
                gain_dict[info[0]] = {}
            if info[0] not in res_dict:
                res_dict[info[0]] = []

            res_dict[info[0]].append(info[2])  # info[2]=tweet_id

            if int(info[3]) > 0:  # info[3]=gain
                gain_dict[info[0]][info[2]] = int(info[3])

    return gain_dict, res_dict


def MAP_eval(gain_dict, res_dict, k=100):
    '''Mean Average Precision'''
    pass


def MRR_eval(gain_dict, res_dict, k=100):
    '''Mean Reciprocal Rank'''
    pass


def NDCG_eval(gain_dict, res_dict, k=100):
    '''Normalized Discounted Cumulative Gain'''
    pass
