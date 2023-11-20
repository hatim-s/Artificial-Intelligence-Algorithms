import random

class GeneticAlgorithm:
    def __init__ (
        self, generations=200, population_size=4, chromosome_size=26,
        similarity_criterion="equal", crossover_scheme="random", mutation_rate=1.00,
        mutation_mechanism="swap", stopping_threshold=0.75, verbose=False
    ):
        """
        Initialize the GeneticAlgorithm class with the specified parameters.

        Args:
            generations (int): Number of generations.
            population_size (int): Size of the population.
            chromosome_size (int): Size of each chromosome.
            similarity_criterion (str): Criterion for similarity ("equal", "nearby").
            crossover_scheme (str): Crossover scheme ("midpoint", "random").
            mutation_rate (float): Rate of mutation.
            mutation_mechanism (str): Mutation mechanism ("swap", "become-neighbour").
            stopping_threshold (float): Fitness threshold for stopping the algorithm.
            verbose (bool): Verbosity flag.

        Returns:
            None
        """
        self.generations = generations
        self.population_size = population_size
        self.chromosome_size = chromosome_size
        self.similarity_criterion = similarity_criterion
        self.crossover_scheme = crossover_scheme 
        self.mutation_rate = mutation_rate
        self.mutation_mechanism = mutation_mechanism 
        self.stopping_threshold = stopping_threshold
        self.verbose = verbose

        self.population = None

    def are_similar(self, letter1, letter2):
        """
        Check if two letters are similar.

        Args:
            letter1 (str): First letter to compare.
            letter2 (str): Second letter to compare.

        Returns:
            bool: True if the letters are similar, False otherwise.
        """
        return (
            letter1 == letter2 if self.similarity_criterion == "equal" 
            else abs(ord(letter1) - ord(letter2)) <= 1  # self.similarity_criterion == "nearby"
        )

    def initialize_population(self):
        """
        Initialize a population of chromosomes.

        Returns:
            None
        """
        # Given set of 4 random words, each of length 26
        def generate_random_string(length):
            letters = [random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(length)]
            return ''.join(letters)

        word_set = [
            generate_random_string(self.chromosome_size) 
            for _ in range(self.population_size)
        ]
        print(f"Starting Population:")
        print(word_set, "\n")
        self.population = word_set

    def fitness(self, chromosome):
        """
        Evaluate the fitness of a chromosome based on the arrangement of similar letters.

        Args:
            chromosome (str): The chromosome to evaluate.

        Returns:
            int: The fitness score.
        """
        score = 0
        for i in range(len(chromosome) - 1):
            if self.are_similar(chromosome[i], chromosome[i + 1]):
                score += 2
        return max(score, 1)

    def select_parents(self, fitness_scores):
        """
        Select two parents from the population using roulette wheel selection.

        Args:
            fitness_scores (list): The fitness scores corresponding to each chromosome.

        Returns:
            tuple: Two selected parents.
        """
        total_fitness = sum(fitness_scores)
        probabilities = [fit / total_fitness for fit in fitness_scores]
        
        parent1 = random.choices(self.population, probabilities)[0]
        parent2 = None
        for _ in range(10):
            parent2 = random.choices(self.population, probabilities)[0]
            if parent2 != parent1:
                break

        return parent1, parent2

    def crossover(self, parent1, parent2):
        """
        Perform one-point crossover between two parents to create two children.

        Args:
            parent1 (str): The first parent chromosome.
            parent2 (str): The second parent chromosome.

        Returns:
            tuple: Two children resulting from crossover.
        """
        crossover_point = (
            len(parent1) / 2  if self.crossover_scheme == "midpoint" 
            else random.randint(0, len(parent1))  # self.crossover_scheme == "random"
        )
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2

    def mutate(self, chromosome):
        """
        Introduce mutation in a chromosome by swapping two positions.

        Args:
            chromosome (str): The chromosome to mutate.

        Returns:
            str: The mutated chromosome.
        """
        mutated_chromosome = list(chromosome)

        if self.mutation_mechanism == "swap":
            if random.randint(0, 100) <= self.mutation_rate * 100:
                mutation_point1, mutation_point2 = random.sample(range(len(chromosome)), 2)
                (
                    mutated_chromosome[mutation_point1], 
                    mutated_chromosome[mutation_point2]
                ) = (
                    mutated_chromosome[mutation_point2], 
                    mutated_chromosome[mutation_point1]
                )

        if self.mutation_mechanism == "become-neighbour":
            mutated_chromosome = [
                mutated_chromosome[i] if random.randint(0, 100) > 100 * self.mutation_rate
                else (mutated_chromosome[i+1] if i < len(mutated_chromosome)-1 else mutated_chromosome[i-1])
                for i in range(len(mutated_chromosome))
            ]

        return ''.join(mutated_chromosome)

    def run(self):
        """
        Perform a Genetic Algorithm to find a solution to the given problem.

        Returns:
            None
        """
        population = self.initialize_population()

        for generation in range(self.generations):
            fitness_scores = [self.fitness(chromosome) for chromosome in self.population]

            # Stopping criteria: terminates when max_fitness crosses a particular fractional threshold
            if max(fitness_scores) > self.chromosome_size * self.stopping_threshold:
                print("============================== Final Stage ====================================\n")
                print(f"Solution found in generation {generation}!")
                break

            new_population = []

            for _ in range(self.population_size // 2):
                parent1, parent2 = self.select_parents(fitness_scores)
                child1, child2 = self.crossover(parent1, parent2)

                # Apply mutation
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)

                new_population.extend([child1, child2])

            self.population = new_population

            if self.verbose:
                print(f"=============================== Next Generation: ==============================")
                print(self.population[0], self.population[1])
                print(self.population[2], self.population[3])
                print("\n")

        best_solution = max(self.population, key=self.fitness)
        print(f"Best solution: {best_solution}, Fitness: {self.fitness(best_solution)}")

# Example usage

print("Number of Generations (default = 200)")
print("Population Size (default = 4)")
print("Chromosome Size (default = 26)")
print("Similarity Criterion (default = 'equal')")
print("Crossover Scheme (default = 'midpoint')")
print("Mutation Rate (default = 1.00)")
print("Mutation Mechanism (default = 'swap')")
print("Stopping Factor (default = 0.75)")
verbose = input("\nVerbose? (default = False): ")

print("\n")

if verbose.lower() == "true":
    verbose = True
else:
    verbose = False

solver = GeneticAlgorithm(verbose=verbose)
solver.run()
