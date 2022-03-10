# Author: Floriana Ciaglia
# Date: Jan 25, 2022
# File: This file will hold some database-pipeline connection tests
from os import path
import sys

sys.path.append(path.abspath('/home/FLOCIAGLIA/ForestryServiceDatabase/db/orm_scripts'))

from pipe_get_data import get_most_similar_guess



def main():

    guesses = ['shep', 'cheep', 'sheep']
    field = 'kind of livestock'
    best_match = get_most_similar_guess(guesses, field)
    print("best match: ", best_match)


if __name__ == "__main__":
    main()