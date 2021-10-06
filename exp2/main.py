import argparse
from rankedRetrieval import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default='../dataset/tweets.txt')
    args = parser.parse_args()

    postings, doc_nums = get_postings(args.path)

    while True:
        q = input('input query >> ')
        search(postings, q)


if __name__ == '__main__':
    main()
