#!/usr/bin/env python3

from collections import namedtuple
import random
import string

LETTERS = string.ascii_lowercase
WIDTH = len(LETTERS)

##POPULATION = 200
##TIMESTEPS = 100
POPULATION = 100
TIMESTEPS = 20

Individual = namedtuple('Individual', ['weights', 'fitness'])

def new_weight():
    return (10 * random.random() - 5)

def classify(ind, featvec):
    """Return the answer for this individual trying to classify these
    features."""
    assert len(ind.weights) == len(featvec)
    total = sum(w*xi for w,xi in zip(ind.weights, featvec))
    return total > 0

def fitness(ind, trainingset):
    """Just return the number of instances of the trainingset the individual gets
    right."""
    out = 0
    for instance in trainingset:
        if classify(ind, instance[0]) == instance[1]:
            out += 1
    return out

def initial_population(trainingset):
    out = []
    for i in range(POPULATION):
        weights = []
        for ignore in range(WIDTH):
            weights.append(new_weight())
        fitscore = fitness(Individual(weights, 0), trainingset)
        ind = Individual(weights, fitscore)
        out.append(ind)
    return out

def features(text):
    lower = text.lower()
    return [lower.count(c) for c in LETTERS]

def sample_individual(population):
    population_fitness = sum(ind.fitness for ind in population)
    point = random.randrange(0, population_fitness)
    for ind in population:
        if point < ind.fitness:
            return ind
        point -= ind.fitness
    assert False, "omfg this should not happen"

def optimize(population, trainingset):
    for t in range(TIMESTEPS):
        print("timestep:", t)
        ## sort by fitness
        population.sort(key=lambda ind: ind.fitness, reverse=True)
        print("best fitness:", population[0].fitness)

        ## cull bottom half.
        population = population[:POPULATION // 2]

        ## shuffle it up.
        random.shuffle(population)

        ## mutate about half of the survivors
        for b in range(POPULATION // 4):
            i = random.randrange(0,POPULATION//2)
            j = random.randrange(0,WIDTH)
            population[i].weights[j] = new_weight()

        ## cross some over
        newgen = []
        for b in range(POPULATION // 2):
            ## pick two of them to cross, build a new one!
            mom = sample_individual(population)
            dad = sample_individual(population)
            cross = random.randrange(0, WIDTH)
            weights = mom.weights[:cross] + dad.weights[cross:]
            fitscore = fitness(Individual(weights, 0), trainingset)
            baby = Individual(weights, fitscore)
            newgen.append(baby)
        population.extend(newgen)
    return population[0]

def instances(s):
    """Given a string, maybe the contents of a line-delimited file, return all
    of the feature vectors for each line in that string."""
    out = []
    lines = s.split("\n")
    for line in lines:
        line = line.strip()
        if not line: continue
        out.append(features(line))
    return out

def letter_info(ind):
    pos = []
    neg = []
    for i,c in enumerate(LETTERS):
        if ind.weights[i] > 0:
            pos.append(c)
        else:
            neg.append(c)
    print("positive (es):", "".join(pos))
    print("negative (en):", "".join(neg))

def main():
    en_texts = open("thousand.en.txt").read()
    es_texts = open("thousand.es.txt").read()
    trainingset = []
    for fv in instances(en_texts):
        trainingset.append((fv, False))
    for fv in instances(es_texts):
        trainingset.append((fv, True))

    population = initial_population(trainingset)
    best = optimize(population, trainingset)
    letter_info(best)

    ## now do a test set!!
    en_texts = open("lastthousand.en.txt").read()
    es_texts = open("lastthousand.es.txt").read()
    testset = []
    for fv in instances(en_texts):
        testset.append((fv, False))
    for fv in instances(es_texts):
        testset.append((fv, True))

    testset_score = fitness(best, testset)
    print("score on test set:", testset_score)

if __name__ == "__main__": main()
