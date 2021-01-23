"""gene class module"""
import random


class Genome():
    """genes assigned to each individual and changed upon breeding and mutation"""

    def __init__(self, aggro=0):
        self.dna = {
            'aggro': aggro
        }
        self.mutate()

    def mutate(self):
        """random chance of gene mutation"""
        flip = {0 : 1, 1 : 0}
        rand = random.randint(1, 100)
        if rand < 5:
            self.dna['aggro'] = flip[self.dna['aggro']]
