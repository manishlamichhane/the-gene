from defaults import Threshold
from nature import Nature
from stats import Statistics

def generate_stats(nature):
    stats = Statistics(nature)
    stats.display()
if __name__ == "__main__":
    nature = Nature()
    round = 1
    while not nature.total_population >= Threshold.POPULATION:
        print(f'Round: {round}')
        nature.enforce_darwinism()
        nature.select()
        if not len(nature.male_population) >= 2:
            Statistics(nature).display()
            print('Best Male Identified: ')
            print(nature.male_population[0].__dict__)
            break
        nature.age()
        round += 1
        Statistics(nature).display()
