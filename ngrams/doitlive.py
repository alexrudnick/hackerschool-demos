#!/usr/bin/env python3

import math
import sys
import random
import readline

from collections import defaultdict
from collections import Counter

LOW_NUMBER = 0.00001

## counts dictionary maps from contexts to dictionaries (Counters) that map from
## words to their counts.

def build_counts(sentences):
    """Return a counts dictionary, given a list of sentences."""
    out = defaultdict(Counter)
    for sent in sentences:
        sent = [None] + sent + [None]
        for (prev, cur) in zip(sent, sent[1:]):
            out[prev][cur] += 1
    return out

def counts_to_probs(counts_dict):
    """Take a counts dictionary and return the appropriate probs dictionary."""
    out = defaultdict(lambda: defaultdict(lambda: LOW_NUMBER))
    for prev in counts_dict:
        for cur in counts_dict[prev]:
            out[prev][cur] = (counts_dict[prev][cur] /
                              sum(counts_dict[prev].values()))
    return out

def unigram_probs(sentences):
    counts = Counter()
    out = defaultdict(lambda: LOW_NUMBER)
    for sent in sentences:
        for cur in sent:
            counts[cur] += 1
    total_words = sum(counts.values())
    for word,count in counts.items():
        out[word] = count / total_words
    return out

def get_sentences(fn):
    with open(fn) as infile:
        out = infile.readlines()
        out = [line.strip().split() for line in out]
    return out

def sample_word(word_dist):
    """Given a little distribution dictionary, sample one word."""
    score = random.random()
    for word,prob in word_dist.items():
        if score < prob:
            return word
        score -= prob
    assert False, "this should also never happen"

def sample_sentence(probs_dict):
    """Generate a sentence!!"""
    prev = None
    out = []
    while True:
        cur = sample_word(probs_dict[prev])
        if cur is None:
            return out
        out.append(cur)
        prev = cur
    assert False, "this should never happen!"

def score_sentence(sent, bigram_probs, unigram_probs):
    """Return the surprisal value of this sentence in bits."""
    total_surprise = 0

    sent = [None] + sent + [None]
    for (prev, cur) in zip(sent, sent[1:]):
        if prev in bigram_probs and cur in bigram_probs[prev]:
            surprise = -math.log(bigram_probs[prev][cur], 2)
        else:
            ## STUPID BACKOFF (Brants et al 2010)
            prob = 0.4 * unigram_probs[cur]
            surprise = -math.log(prob, 2)
        total_surprise += surprise
    return total_surprise

def main():
    sentences = get_sentences(sys.argv[1])
    counts = build_counts(sentences)

    bigram = counts_to_probs(counts)
    unigram = unigram_probs(sentences)



    ##print(sentence)
    ##print(" ".join(sentence))
    sent = "`` What ho , Angela , old girl . ''".split()
    print(sent)
    score = score_sentence(sent, bigram, unigram)
    print(score)

    sent = "`` What airplane , Angela , old girl . ''".split()
    print(sent)
    score = score_sentence(sent, bigram, unigram)
    print(score)

    print("GIVE ME SENTENCES.")
    while True:
        line = input("> ")
        if not line: break
        sent = line.split()
        score = score_sentence(sent, bigram, unigram)

        print("I give it a:", score)
        generated = sample_sentence(bigram)
        print("Let me try: ", " ".join(generated))
        score = score_sentence(generated, bigram, unigram)
        print("I got a:", score) 

if __name__ == "__main__": main()
