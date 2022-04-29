# Author: Floriana Ciaglia
# Date: Feb 1st, 2022
# File: This file holds functions that interact with the OCR pipeline

# This file will act as main. We'll call all Sandra's functions from here. 

from collections import Counter
from math import sqrt
import re
from config import DATABASE_URI
from query_db import get_valid_opts
from create_validation_tables import Session, engine, Base, ValidForest, ValidAllotment, ValidLivestock, ValidRangerDist


local_session = Session(bind=engine)


def word2vec(word):

    # count the characters in word
    cw = Counter(word)
    # precomputes a set of the different characters
    sw = set(cw)
    # precomputes the "length" of the word vector
    lw = sqrt(sum(c*c for c in cw.values()))

    # return a tuple
    return cw, sw, lw

def cosdis(v1, v2):
    # which characters are common to the two words?
    common = v1[1].intersection(v2[1])
    # by definition of cosine distance we have
    return sum(v1[0][ch]*v2[0][ch] for ch in common)/v1[2]/v2[2]


# the guesses list comes from the pipeline side
# the valid options come from the database
def get_most_similar_guess(ocr_guess, field_name): 
    '''
        This function will be called from the
        pipeline to receive the most similar
        guess of word for each field in the form.
    '''

    field_valid_opts = get_valid_opts(field_name, local_session)
    # print("Valid options:", field_valid_opts)
    best_match = [0, ]

    word = ''.join(ocr_guess).lower()
    word = re.sub(r"\s+", "", word)
    # print("passed in", word)


    for poss in field_valid_opts:
        # print(poss)
        va = word2vec(word)
        vb = word2vec(poss)
        
        prob = cosdis(va, vb)

        if prob > best_match[0]: # we probably found a match
            best_match = [prob, poss]
        # print("at this stage", best_match)


    if best_match[0] == 0.0:
        return 'null' 
     
 
    return best_match[1]



def main():

    best_match = get_most_similar_guess(['hors', 'hoirse', 'hors'], 'kind of livestock')
    # print(best_match)
    print("--- The best match is", best_match)


if __name__ == '__main__':
    main()
