from random import *
from Generation import *
from Evolution import *
from configparser import ConfigParser
import json
import csv
import copy

# tu nacitavam udaje z mojho config suboru
config = ConfigParser()
config.read("config.ini")

max_x = int(config['GARDEN']['width'])
max_y = int(config['GARDEN']['depth'])
stones = json.loads(config['GARDEN']['stones'])

max_monks = int(config['EVOLUTION']['generation_size'])
max_parents = int(config['EVOLUTION']['max_parents'])
max_children = int(config['EVOLUTION']['max_children'])
mutation_chance = int(config['EVOLUTION']['mutation_chance'])

selection = int(config['SELECTION']['type'])


# funkcia, ktora na zaciatku vytvori mapu
def create_garden():
    garden = [[0 for _ in range(max_x)] for _ in range(max_y)]

    for i in range(0, max_y):
        for j in range(0, max_x):
            for stone in stones:
                if stone[0] == j and stone[1] == i:
                    garden[i][j] = -1  # za kazdy kamen da -1

    return garden


def print_garden(garden):

    for i in range(0, max_y):
        for j in range(0, max_x):
            print(garden[i][j], " ", end=" ")

        print("")
    print("")


# funkcia, ktora pozera ci sa moze mnich posunut do daneho smeru
def can_move(garden, direction, x, y):

    if direction == "RIGHT":
        if x < max_x - 1 and garden[y][x + 1] == 0 or x + 1 == max_x:
            return True

    elif direction == "LEFT":
        if x > 0 and garden[y][x - 1] == 0 or x - 1 < 0:
            return True

    elif direction == "DOWN":
        if y < max_y - 1 and garden[y + 1][x] == 0 or y + 1 == max_y:
            return True

    elif direction == "UP":
        if y > 0 and garden[y - 1][x] == 0 or y - 1 < 0:
            return True

    return False


# funkcia, ktora pozera ci je mnich stale v mape
def in_map(direction, x, y):

    if direction == "RIGHT" and x < max_x - 1:
        return True

    if direction == "LEFT" and x > 0:
        return True

    if direction == "UP" and y > 0:
        return True

    if direction == "DOWN" and y < max_y - 1:
        return True

    return False


# pri pohybe mnich ziskava nove suradnice
def get_new_coordinates(direction, x, y):

    if direction == "RIGHT" and x + 1 != max_x:
        return x + 1, y

    elif direction == "LEFT" and x - 1 != -1:
        return x - 1, y

    elif direction == "UP" and y - 1 != -1:
        return x, y - 1

    elif direction == "DOWN" and y + 1 != max_y:
        return x, y + 1

    else:
        return x, y


# funkcia, ktora vrati nahodny smer z dvoch zadanych
def get_random_direction(directions):
    return directions[random.randrange(0, 2)]


# ziskavam smer mnicha podla toho z akeho kraja zahrady do nej vchadza
# teda ak ide napriklad vstupit z laveho kraja zahrady dostane smer doprava
def get_direction(x, y):

    if x == 0 and y != 0 and y != max_y - 1:
        return "RIGHT"

    if x == max_x - 1 and y != 0 and y != max_y - 1:
        return "LEFT"

    if y == 0 and x != 0 and x != max_x - 1:
        return "DOWN"

    if y == max_y - 1 and x != 0 and x != max_x - 1:
        return "UP"

    if x == 0 and y == 0:
        return get_random_direction(["DOWN", "RIGHT"])

    if x == 0 and y == max_y - 1:
        return get_random_direction(["UP", "RIGHT"])

    if x == max_x - 1 and y == 0:
        return get_random_direction(["DOWN", "LEFT"])

    if x == max_x - 1 and y == max_y - 1:
        return get_random_direction(["UP", "LEFT"])


# ak mnich dojde k nejakej prekazke musi zmenit smer
# pri vybere noveho smeru sa pozeram na preferovany smer mnicha
# ktory ma nastaveny ako gen
def get_different_direction(direction, preferred_dir):

    if direction == "UP" and preferred_dir == "RIGHT":
        return "RIGHT"

    if direction == "UP" and preferred_dir == "LEFT":
        return "LEFT"

    if direction == "DOWN" and preferred_dir == "RIGHT":
        return "LEFT"

    if direction == "DOWN" and preferred_dir == "LEFT":
        return "RIGHT"

    if direction == "RIGHT" and preferred_dir == "LEFT":
        return "UP"

    if direction == "RIGHT" and preferred_dir == "RIGHT":
        return "DOWN"

    if direction == "LEFT" and preferred_dir == "RIGHT":
        return "UP"

    if direction == "LEFT" and preferred_dir == "LEFT":
        return "DOWN"


# funkcia, ktora pre kazdeho mnicha v danej generacii
# pohrabe zahradu podla chromozomu daneho mnicha
# ak ma jeden z mnichov fitness 100, teda pohrabal celu zahradu
# funkcia vrati danu zahradu, inak vrati None
def rake_garden(original_garden, generation):
    i = 1

    for monk in generation:
        used_entrances = []  # pole, kde si udrziavam uz pouzite vchody do zahrady
        stuck = False
        invalid_move = False  # invalid move je vtedy, ked je rovanky gen ako predtym
        move_number = 1
        gene_index = 0

        garden = copy.deepcopy(original_garden)

        # pokial sa mnich nezasekol alebo este ma nejake nepouzite geny v chromozome
        while not stuck and gene_index != len(monk.chromosome):
            # ziskavam gen z chromozomu
            current_x = monk.chromosome[gene_index][0]
            current_y = monk.chromosome[gene_index][1]

            # ak som tento gen este nepouzil dam ho do pouzitych
            if [current_x, current_y] not in used_entrances:
                used_entrances.append([current_x, current_y])
            # inak idem na dalsi gen
            else:
                gene_index += 1
                continue

            direction = get_direction(current_x, current_y)

            # mnich hrabe pokial je v mape
            while in_map(direction, current_x, current_y):
                # ak sa moze pohnut do daneho smeru, tak sa pohne
                if can_move(garden, direction, current_x, current_y):
                    garden[current_y][current_x] = move_number

                    current_x, current_y = get_new_coordinates(direction, current_x, current_y)

                    if [current_x, current_y] not in used_entrances:
                        used_entrances.append([current_x, current_y])
                    else:
                        invalid_move = True
                        break
                # ak sa nemoze pohnut, pozera ci moze zmenit smer
                else:
                    direction = get_different_direction(direction, monk.preferred_direction)

                    if not can_move(garden, direction, current_x, current_y):
                        if direction == "UP":
                            direction = "DOWN"

                        elif direction == "DOWN":
                            direction = "UP"

                        elif direction == "RIGHT":
                            direction = "LEFT"

                        elif direction == "LEFT":
                            direction = "RIGHT"

                        # ak nemoze mnich zabocit ani do jednej ani do druhej strany
                        # tak sa zasekol a posuvam sa na dalsieho mnicha v generacii
                        if not can_move(garden, direction, current_x, current_y):
                            stuck = True
                            break

            if not invalid_move:
                if current_x != max_x and current_y != max_y and garden[current_y][current_x] != -1:
                    garden[current_y][current_x] = move_number

                move_number += 1
            gene_index += 1

        # vzdy na konci, ked je mnichova zahrada pohrabana nastavim mu
        # fitness podla toho ako zahradu pohrabal
        monk.set_fitness(garden)

        if monk.fitness == 100:
            return garden

        i += 1

    return None


# funkcia na vyber jedincov, ktori budu rodicia
def roulette(fitness_sum, generation):
    pick = random.randrange(0, fitness_sum)
    current_fitness = 0

    for monk in generation:
        current_fitness += monk.fitness
        if current_fitness >= pick:
            return monk


# funkcia, ktora vrati mnicha, s najvacsim fitness
def get_best(monks):
    best = 0
    best_monk = None

    for monk in monks:
        if monk.fitness >= best:
            best = monk.fitness
            best_monk = monk

    return best_monk.chromosome


# funkcia na vyber jedincov, ktori budu rodicia
# vyber je na baze turnaju
def tournament(generation):
    monks = []
    parents = []

    for i in range(0, max_parents):
        for j in range(0, 20):
            monks.append(generation[random.randrange(0, len(generation))])

        parents.append(get_best(monks))

    return parents


# funkcia, ktora vrati pole rodicov, ktori sa budu krizit
def get_parents(generation):
    parents = []
    fitness_sum = 0

    # selection type 1 == tournament selection
    if selection == 1:
        parents = tournament(generation)

    # selection type 2 == roulette selection
    elif selection == 2:
        for monk in generation:
            fitness_sum += monk.fitness

        for i in range(0, max_parents):
            parent = roulette(fitness_sum, generation)

            if parent is not None:
                parents.append(parent.chromosome)
                generation.remove(parent)
                fitness_sum -= parent.fitness

    return parents


# funkcia, ktora generuje novu generaciu mnichov
def generate_new_generation(curr_generation, garden):
    new_generation = []
    evo = Evolution(max_x, max_y, mutation_chance)
    gen = Generation(garden, stones, max_x, max_y, mutation_chance)

    gen_num = curr_generation[0].generation + 1  # cislo novej generacie

    # ziskavam rodicov, bud pomocou rulety alebo turnaja
    parents = get_parents(curr_generation)

    # tu vytvaram potomkov
    for i in range(0, max_children):
        # z rodicov nahodne vyberiem dvoch
        par_index = random.randrange(0, len(parents) - 1)
        other_index = random.randrange(0, len(parents) - 1)

        while other_index == par_index:
            other_index = random.randrange(0, len(parents) - 1)

        # vytvaram potomka
        child = evo.crossover(parents[par_index], parents[other_index], gen_num)

        new_generation.append(child)

    # pokial nemam dostatok jedincov v generacii, pridam uplne novych
    while len(new_generation) < max_monks:
        new_generation.append(gen.create_monk(gen_num))

    return new_generation


def main():
    averages = []
    gen_num = 1

    original_garden = create_garden()
    print_garden(original_garden)

    gen = Generation(original_garden, stones, max_x, max_y, mutation_chance)

    generation = gen.generate_first_generation(max_monks)

    garden = rake_garden(original_garden, generation)

    # vytvaram nove generacie a hrabem zahrady pokial som nenasiel cielovy stav
    while garden is None:
        generation = generate_new_generation(generation, original_garden)
        garden = rake_garden(original_garden, generation)

        fit_sum = 0
        for monk in generation:
            fit_sum += monk.fitness

        average = round(fit_sum / max_monks)
        averages.append([gen_num, average])

        gen_num += 1

    # vypis pohrabanej zahrady
    print("#################")
    print(gen_num, ". generation")
    print_garden(garden)

    # zapisovanie do .csv suboru, ktory pouzivam na vytvorenie grafu v exceli
    with open('mycsv.csv', 'w', newline='') as f:
        f.truncate()
        the_writer = csv.writer(f, delimiter=';')

        for i in range(0, len(averages)):
            if i == 0:
                the_writer.writerow(["Generacia", "Priemer fitness"])
            the_writer.writerow([averages[i][0], averages[i][1]])

main()