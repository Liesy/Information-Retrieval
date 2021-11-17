import argparse
from evaluation import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default='../dataset/qrels2014.txt')
    args = parser.parse_args()

    relevant_gain_dict, retrival_dict = process_data(args.path)
    MAP = MAP_eval(relevant_gain_dict, retrival_dict, 100)
    MRR = MRR_eval(relevant_gain_dict, retrival_dict, 100)
    NDCG = NDCG_eval(relevant_gain_dict, retrival_dict, 100)

    print('MAP = ', round(MAP,3), sep='')
    print('MRR = ', round(MRR,3), sep='')
    print('NDCG = ', round(NDCG,3), sep='')


if __name__ == '__main__':
    main()