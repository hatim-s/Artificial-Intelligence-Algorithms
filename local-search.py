# 4-Queens Problem 
# (solved as a Constraint Satisfaction Problem, 
# using Local-Search with Hill Climbing algorithm)

# Great! Now make a similar report for the following code as well. 
# This source code implements a Genetic Algorithm to solve a problem where 

import random

class NQueensSolver:
    """Class designed to solve a N-Queens problem with N or less queens by
    modelling the problem as a Constraint Satisfaction problem."""

    def __init__(
        self, n_queens:int = 4, verbose:bool = False
    ):
        """Initialize the NQueensSolver object with the specified parameters.

        Parameters:
        - n_queens (int): The number of queens for the N-Queens problem.
        - verbose (bool): If True, print intermediate steps during the solving process.
        """
        self.n_queens = n_queens
        self.verbose = verbose
        self.chessboard = None
    
    def print_chessboard (self):
        """Print the current state of the chessboard."""
        for row in range(self.n_queens):
            for col in range(self.n_queens):
                if self.chessboard[row][col] == '0':
                    print(".", end=" ")
                elif self.chessboard[row][col] == '1':
                    print("Q", end=" ")
                else:
                    print("q", end=" ")
            print()
        print()

    def initial_configuration (self, input_config:list):
        """Parse input_config and assign it to self.chessboard.

        Parameters:
        - input_config (list): List of strings representing the initial chessboard configuration.
        """
        self.chessboard = [row.split() for row in input_config]

        for row in self.chessboard:
            for cell in row:
                if cell not in ['0', '1', "0", "1"]:
                    print(row, "+", cell)
                    print('\n[ERR] Invalid configuration!')
                    exit()
        
        print("\n================================================================================\n")
        print("Input Chessboard:\n")
        self.print_chessboard()

        self.add_queens()
        print("Added remaining queens: (in random position)\n")
        self.print_chessboard()

    def place_random_queen(self):
        """Place a queen randomly on the chessboard."""
        rows = [i for i in range(self.n_queens)]
        cols = [i for i in range(self.n_queens)]

        random.shuffle(rows)
        random.shuffle(cols)

        for row in rows:
            for col in cols:
                if self.chessboard[row][col] == '0':
                    self.chessboard[row][col] = '2'
                    return

    def add_queens (self):
        """Add queens to the chessboard in random positions."""
        count_queens = sum(row.count('1') for row in self.chessboard)
        for _ in range (self.n_queens - count_queens):
            self.place_random_queen()
                        
    def calculate_clashes (self):
        """Calculate the number of clashes in the current configuration."""
        clashes = 0
        for q1_row in range(self.n_queens):
            for q1_col in range(self.n_queens):
                # if there is no queen at (row, col)
                if (self.chessboard[q1_row][q1_col] == '0'):
                    continue

                for q2_row in range(self.n_queens):
                    for q2_col in range(self.n_queens):
                        # if there is no queen at (row, col)
                        if (self.chessboard[q2_row][q2_col] == '0' or
                            (q1_row == q2_row and q1_col == q2_col)):
                            continue

                        if (q1_row == q2_row or q1_col == q2_col):
                            clashes += 1

                        if abs(q1_row - q2_row) == abs(q1_col - q2_col):
                            clashes += 1
        return clashes

    def move_row (self, row, skip):
        """Move a queen in a particular row to a new position."""
        min_clashes = 1e9
        best_row_move = None

        cols = [i for i in range(self.n_queens)]
        random.shuffle(cols)
        for col in cols:
            if (col == skip or self.chessboard[row][col] == '1'
                or self.chessboard[row][col] == '2'):
                continue

            self.chessboard[row][col] = '2'
            new_config_clashes = self.calculate_clashes()
            self.chessboard[row][col] = '0'
        
            if new_config_clashes < min_clashes:
                min_clashes = new_config_clashes
                best_row_move = [row, col]

        return min_clashes, best_row_move        

    def move_col (self, col, skip):
        """Move a queen in a particular column to a new position."""
        min_clashes = 1e9
        best_column_move = None

        rows = [i for i in range(self.n_queens)]
        random.shuffle(rows)
        for row in rows:
            if (row == skip or self.chessboard[row][col] == '1' 
                or self.chessboard[row][col] == '2'):
                continue

            self.chessboard[row][col] = '2'
            new_config_clashes = self.calculate_clashes()
            self.chessboard[row][col] = '0'
        
            if new_config_clashes < min_clashes:
                min_clashes = new_config_clashes
                best_column_move = [row, col]

        return min_clashes, best_column_move

    def best_neighbour (self):
        """
        Find the best neighbor by considering moves in both rows and columns.
        
        Returns
        - min_clashes: minimum number of clashes from all neighbours
        - best_neighbour: the neighbour with minimum number of clashes
        """
        min_clashes = 1e9
        best_neighbour = None

        rows = [i for i in range(self.n_queens)]
        cols = [i for i in range(self.n_queens)]

        random.shuffle(rows)
        random.shuffle(cols)

        for row in rows:
            for col in cols:
                if self.chessboard[row][col] != '2':
                    continue

                self.chessboard[row][col] = '0'
                
                new_min_clashes, new_best_neighbour = self.move_row(row, skip=col)
                if new_min_clashes < min_clashes:
                    min_clashes = new_min_clashes
                    best_neighbour = [[row, col], new_best_neighbour]

                new_min_clashes, new_best_neighbour = self.move_col(col, skip=row)
                if new_min_clashes < min_clashes:
                    min_clashes = new_min_clashes
                    best_neighbour = [[row, col], new_best_neighbour]

                self.chessboard[row][col] = '2'

        return min_clashes, best_neighbour

    def update_configuration (self):
        """Update the current configuration to a new configuration with fewer clashes."""
        current_clashes = self.calculate_clashes()
        min_clashes, best_neighbour = self.best_neighbour()

        if min_clashes <= current_clashes:
            old_row, old_col = best_neighbour[0][0], best_neighbour[0][1] 
            new_row, new_col = best_neighbour[1][0], best_neighbour[1][1]

            self.chessboard[old_row][old_col] = '0'
            self.chessboard[new_row][new_col] = '2'

            # Handling an edge case where min_clashes 
            # can become 0 and the loop might still continue.
            if min_clashes == 0:
                return -1
            if min_clashes == current_clashes:
                return 0
            return 1

        return -1

    def local_search(self):
        """Perform local search using the Hill Climbing algorithm."""
        counter, flag = 0, 0
        while True:
            flag = self.update_configuration()

            if self.verbose:
                self.print_chessboard()

            if flag == -1:
                break

            if flag == 1:
                counter = 0
                continue

            counter += 1
            if counter >= 10:
                break

        return self.chessboard

# User Input Section
print("""Input initial chessboard configuration: 
1. Use 0s to denote empty squares and 1s to denote queens
2. Use spaces as separators
3. Input at max 3 queens
""")
chessboard = [input() for _ in range(4)]

verbose = input("\nVerbose? (default = False): ")
if verbose.lower().strip() == "true":
    verbose = True
else:
    verbose = False

# Solve the N-Queens problem using local search
nqueens = NQueensSolver(4, verbose=verbose)
nqueens.initial_configuration(chessboard)

print ("\n================================================================================\n")
print("Solving the board as a Constraint Satisfaction Problem using Local Search \n")

chessboard = nqueens.local_search()

print ("\n================================================================================\n")
print("Output State:\n")
nqueens.print_chessboard()
