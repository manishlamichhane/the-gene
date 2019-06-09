from defaults import Index


class Statistics:
    def __init__(self, nature, **kwargs):
        self.nature = nature
        self.population = nature.male_population + nature.female_population
    
    def _calculate_fitness_percent(self, population):
        counter = 0
        for individual in population:
            if individual.fitness >= Index.FITNESS:
                counter += 1
        return counter / len(population) * 100

    def calculate_total_fit_percent(self):
        if not self.population:
            return 0
        return self._calculate_fitness_percent(self.population)
    
    def calculate_total_fit_male_percent(self):
        if not self.nature.male_population:
            return 0
        return self._calculate_fitness_percent(self.nature.male_population)
    
    def calculate_total_fit_female_percent(self):
        if not self.nature.female_population:
            return 0
        return self._calculate_fitness_percent(self.nature.female_population)

    def display(self):
        print('##########################')
        print(f'Total Population: {self.nature.total_population}')
        print(f'Total Fit Population %: {self.calculate_total_fit_percent()}')
        print(f'Total Male: {len(self.nature.male_population)}')
        print(f'Total Fit Male %: {self.calculate_total_fit_male_percent()}')
        print('')
        print(f'Total FeMale: {len(self.nature.female_population)}')
        print(f'Total Fit FeMale %: {self.calculate_total_fit_female_percent()}')
        print('##########################')
