import random

class Population:
    def __init__(self, population_size, mutation_rate, genes, chromosome_len):
        self.generation = 1
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.genes = genes
        self.chromosome_len = chromosome_len
        self.population = [Individual.create(self.genes, self.chromosome_len)
            for _ in range(self.population_size)]
        self.sorted = False
    
    def calculate_fitness(self, target):
        for individual in self.population:
            individual.calculate_fitness(target)
    
    def get_best_individual(self):
        self.sort_population_by_fitness_if_needed()
        return self.population[0]

    def sort_population_by_fitness_if_needed(self):
        if not self.sorted:
            self.sort_population_by_fitness()

    def sort_population_by_fitness(self):
        self.population.sort(key=lambda x:x.fitness, reverse=True)
        self.sorted = True

    def create_new_generation(self):
        new_generation = []
        one_tenth_population = self.population_size // 10
        half_population = self.population_size // 2
        new_generation.extend(self.population[:one_tenth_population])
        for _ in range(self.population_size - one_tenth_population):
            parent1 = random.choice(self.population[:half_population])
            parent2 = random.choice(self.population[:half_population])
            child = parent1.mate(parent2)
            if random.random() <= self.mutation_rate:
                child.mutate(self.genes)
            new_generation.append(child)
        self.population = new_generation
        self.generation += 1
        self.sorted = False
    
    def print_best(self):
        best_individual = self.get_best_individual()
        print(f'Generation: {self.generation}\tString: {"".join(best_individual.chromosome)}\tFitness: {best_individual.fitness}')
    
    def found_solution(self, target_fitness):
        best_individual = self.get_best_individual()
        return best_individual.fitness >= target_fitness


class Individual:
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = 0
    
    @staticmethod
    def create(genes, chromosome_len):
        chromosome = [random.choice(genes) for _ in range(chromosome_len)]
        return Individual(chromosome)
    
    def mate(self, parent):
        parents_genes = zip(self.chromosome, parent.chromosome)
        choose_gene = lambda g1,g2: g1 if random.random() < 0.5 else g2
        chromosome = [choose_gene(g1, g2) for g1, g2 in parents_genes]
        return Individual(chromosome)
    
    def mutate(self, genes):
        gene_to_mutate = random.choice(range(len(self.chromosome)))
        self.chromosome[gene_to_mutate] = random.choice(genes)

    def calculate_fitness(self, target):
        self.fitness = 0
        for my_gene, target_gene in zip (self.chromosome, target):
            if my_gene == target_gene:
                self.fitness += 1

def main():
    population_size = 1000
    mutation_rate = .01
    genes = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890, .-;:_!"#%&/()=?@${[]}'
    target = 'There are no Wolves on Fenris.'

    population = Population(population_size, mutation_rate, genes, len(target))
    while True:
        population.calculate_fitness(target)
        population.print_best()
        if population.found_solution(target_fitness=len(target)):
            break
        population.create_new_generation()

if __name__ == '__main__':
    main()