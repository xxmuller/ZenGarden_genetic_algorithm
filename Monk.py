import random


class Monk:
    chromosome = []
    preferred_direction = ""
    fitness = 0
    max_x = 0
    max_y = 0
    directions = ["LEFT", "RIGHT"]
    generation = 0

    def __init__(self, generation, chromosome, max_x, max_y):
        self.generation = generation
        self.chromosome = chromosome
        self.preferred_direction = self.directions[random.randrange(0, 2)]
        self.max_x = max_x
        self.max_y = max_y

    # funkcia, ktora danemu objektu mnicha nastavi fitness
    # podla toho kolko policok v zahrade pohrabal
    def set_fitness(self, garden):
        total_num_of_blocks = 0
        num_of_raked_blocks = 0

        for i in range(0, self.max_y):
            for j in range(0, self.max_x):

                if garden[i][j] != -1:
                    total_num_of_blocks += 1

                    if garden[i][j] != 0:
                        num_of_raked_blocks += 1

        # fitness mnicha udavam v percentach, pretoze sa mi s nimi lahsie pracuje
        self.fitness = round((num_of_raked_blocks / total_num_of_blocks) * 100)


