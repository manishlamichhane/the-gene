from defaults import Threshold
from nature import Nature
from stats import Statistics

if __name__ == "__main__":
    round = 1
    nature = Nature()
    stats = Statistics(nature)
    fertile_male = stats.get_fertile_male_pop()
    fertile_female = stats.get_fertile_female_pop()

    while not nature.total_population >= Threshold.POPULATION and fertile_female > 0 and fertile_male > 0:
        print(f'Round: {round}')
        nature.enforce_darwinism()
        nature.select()
        
        if not len(nature.male_population) is 1:
            stats.display()
            print('Best Male Identified: ')
            print(nature.male_population[0].__dict__)
            break

        nature.age()
        round += 1

        stats.display()
