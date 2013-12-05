#!/usr/bin/env python3

"""
Usage: python3 one_sentence_per_line.py --infn="infile.txt" --outfn="outfile.txt"

Take a text file, use NLTK to segment the sentences and tokenize the words (both
in the default NLTK way), then print out one sentence per line with the words
already tokenized, into the specified output file.
"""

import argparse

import nltk

def get_argparser():
    """Build the argument parser for main."""
    parser = argparse.ArgumentParser(description='memmwsd')
    parser.add_argument('--infn', type=str, required=True)
    parser.add_argument('--outfn', type=str, required=True)
    parser.add_argument('--tokenize',dest='tokenize',action='store_true')
    parser.add_argument('--no-tokenize',dest='tokenize',action='store_false')
    parser.set_defaults(tokenize=True)
    return parser

def main():
    parser = get_argparser()
    args = parser.parse_args()

    with open(args.infn) as infile:
        text = infile.read()
        text = text.replace("\n\n", "[[[PARAGRAPHBREAK]]]")
        text = text.replace("\n", " ")
        text = text.replace("[[[PARAGRAPHBREAK]]]", "\n\n")

    sentences = nltk.sent_tokenize(text)
    with open(args.outfn, "w") as outfile:
        for sent in sentences:
            sent = sent.strip()
            if not sent: continue
            if args.tokenize:
                toks = nltk.word_tokenize(sent)
                print(" ".join(toks), file=outfile)
            else:
                print(sent, file=outfile)

if __name__ == "__main__": main()
