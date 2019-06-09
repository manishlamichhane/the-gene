from defaults import Threshold
from nature import Nature
from stats import Statistics

def generate_stats(nature):
    stats = Statistics(nature.male_population, nature.female_population)
    print('##########################')
    print(f'Total Population: {nature.total_population}')
    print(f'Total Fit Population %: {stats.calculate_total_fit_percent()}')
    print(f'Total Male: {len(nature.male_population)}')
    print(f'Total Fit Male %: {stats.calculate_total_fit_male_percent()}')
    print('')
    print(f'Total FeMale: {len(nature.female_population)}')
    print(f'Total Fit FeMale %: {stats.calculate_total_fit_female_percent()}')
    print('##########################')

if __name__ == "__main__":
    nature = Nature()
    round = 1
    while not nature.total_population >= Threshold.POPULATION:
        print(f'Round: {round}')
        nature.enforce_darwinism()
        nature.select()
        if not len(nature.male_population) >= 2:
            generate_stats(nature)
            print('Best Male Identified')
            print(nature.male_population[0].__dict__)
            break
        nature.age()
        round += 1
        generate_stats(nature)
