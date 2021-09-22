import argparse
from index import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default='../dataset/tweets.txt')
    args = parser.parse_args()

    index = inverted_index(args.path)


if __name__ == '__main__':
    main()
