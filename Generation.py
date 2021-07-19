from Evolution import *


class Generation:
    garden = []
    stones = []
    max_x = 0
    max_y = 0
    generation = []
    chromosome_length = 0
    mutation = 0

    def __init__(self, garden, stones, max_x, max_y, mutation):
        self.garden = garden
        self.stones = stones
        self.max_x = max_x
        self.max_y = max_y
        self.mutation = mutation
        self.chromosome_length = max_x + max_y + len(stones)

    # vytvaram chromozom pre mnicha
    def generate_chromosome(self):
        chromosome = []
        evo = Evolution(self.max_x, self.max_y, self.mutation)

        # kazdy chromozom sa sklada z nahodnych vstupov do zahrady
        for i in range(0, self.chromosome_length):
            gene = evo.get_random_gene()

            # ak je na danom vstupe nahodou kamen, tak vytvorim novy nahodny gen
            while self.garden[gene[1]][gene[0]] == -1:
                gene = evo.get_random_gene()

            chromosome.append(gene)

        return chromosome

    def create_monk(self, gen_num):
        chromosome = self.generate_chromosome()
        monk = Monk(gen_num, chromosome, self.max_x, self.max_y)

        return monk

    # funkcia na vytvorenie prvej generacie mnichov
    def generate_first_generation(self, max_monks):
        for i in range(0, max_monks):
            self.generation.append(self.create_monk(1))

        return self.generation

    def print_generation(self, generation):
        i = 1
        for monk in generation:
            print(i, ". ", monk.chromosome, " direction = ", monk.preferred_direction)
            i += 1