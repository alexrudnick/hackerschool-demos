#!/usr/bin/env python3

import sys
import readline

import nltk

def load_words(fn):
    """Get all the space-seperated words from a specified text file, so we can
    build an NLTK Text object out of it next."""
    words = []
    with open(fn) as infile:
        for line in infile:
            words.extend(line.strip().split())
    return words

def main():
    fn = sys.argv[1]
    words = load_words(fn)
    text = nltk.Text(words)

    while True:
        try:
            q = input("search for > ")
        except: break
        if not q: continue
        text.concordance(q, lines=1000)

if __name__ == "__main__": main()
