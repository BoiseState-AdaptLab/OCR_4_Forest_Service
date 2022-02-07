# Author: Floriana Ciaglia
# Date: Jan 25, 2022
# File: This file will hold some database-pipeline connection tests
from os import path
import sys

# sys.path.append(path.abspath('../../../../ForestryServiceDatabase/db/orm_scripts/pipe_get_data'))

from pipe_get_data import get_most_similar_guess

def main():

    guesses = ['shep', 'cheep', 'sheep']
    field = 'kind of livestock'
    get_best_match(guesses, field)


def get_best_match(guesses, field):
    best_match = get_most_similar_guess(guesses, field)
    print("Final return statement: ", best_match)
    return best_match


if __name__ == "__main__":
    main()