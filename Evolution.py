from Monk import *


class Evolution:
    max_x = 0
    max_y = 0
    mutation_chance = 0

    def __init__(self, max_x, max_y, mutation_chance):
        self.max_x = max_x
        self.max_y = max_y
        self.mutation_chance = mutation_chance

    # funkcia, ktora robi krizenie dvoch jedincov
    # a nasledne vracia novovytvoreneho jedinca
    def crossover(self, parent, other, gen_num):
        child_chromosome = []

        # krizeneie prebieha tak, ze zakazdym zoberiem jeden gen z jedneho rodica a dalsi z druheho
        # zakazdym sa moze dany gen zmutovat
        for i in range(0, len(parent)):
            if i % 2 == 0:
                gene = self.possible_mutation(parent[i])
            else:
                gene = self.possible_mutation(other[i])

            child_chromosome.append(gene)

        child = Monk(gen_num, child_chromosome, self.max_x, self.max_y)
        return child

    # funkcia, ktora vytvori nahodny gen, teda nahodny vstup do zahrady
    def get_random_gene(self):
        sides = ["UP", "DOWN", "LEFT", "RIGHT"]
        random_side = sides[random.randrange(0, 4)]

        if random_side == "UP":
            return random.randrange(0, self.max_x), 0

        if random_side == "DOWN":
            return random.randrange(0, self.max_x), self.max_y - 1

        if random_side == "LEFT":
            return 0, random.randrange(0, self.max_y)

        if random_side == "RIGHT":
            return self.max_x - 1, random.randrange(0, self.max_y)

    # funkcia, ktora moze s urcitou pravdepodobnostou zmenit dany gen
    def possible_mutation(self, gene):

        mutation = random.randrange(0, 100)
        if mutation < self.mutation_chance:
            return self.get_random_gene()

        return gene