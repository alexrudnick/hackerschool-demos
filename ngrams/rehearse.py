#!/usr/bin/env python3

import sys
from collections import Counter
from collections import defaultdict

def build_counts(sentences):
    counts = defaultdict(Counter)
    for sent in sentences:
        seq = [None, None] + sent + [None]
        for (pp,p,word) in zip(seq, seq[1:], seq[2:]):
            counts[(pp,p)][word] += 1
    return counts

def counts_to_probs(counts_dict):
    out = defaultdict(dict)
    for key in counts_dict:
        total = sum(counts_dict[key].values())
        for word in counts_dict[key]:
            out[key][word] = counts_dict[key][word] / total
    return out

def get_sentences(infn):
    out = []
    with open(infn) as infile:
        for line in infile:
            line = line.strip()
            sent = line.split()
            out.append(sent)
    return out

import random
def sample(prob_dict):
    pairs = list(prob_dict.items())
    p = random.random()
    for (word, prob) in prob_dict.items():
        if p < prob:
            return word
        p -= prob
    assert False, "this should never happen"

def sample_trigram_sentence(probs):
    pp, p = None, None
    out = []
    while True:
        nextword = sample(probs[(pp,p)])
        if nextword is None: break
        out.append(nextword)
        pp = p
        p = nextword
    return out

def main():
    infn = sys.argv[1] 
    sentences = get_sentences(infn)
    counts = build_counts(sentences)
    trigram_model = counts_to_probs(counts)

    sentence = sample_trigram_sentence(trigram_model)
    print(sentence)

if __name__ == "__main__": main()
