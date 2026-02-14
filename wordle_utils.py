from math import log2

POSSIBLE_SOLUTIONS_PATH: str = 'wordle_solutions.txt'
ALLOWED_GUESSES_PATH: str = 'wordle_allowed_guesses.txt'

def load_words(path: str) -> list[str]:
    with open(path, 'r') as file:
        return [line.strip() for line in file]

def evaluate_guess(guess: str, solution: str) -> tuple[int]:
    solution_chars: list[str] = list(solution)
    pattern: list[int] = [0] * 5
    # Greens
    for i in range(5):
        if guess[i] == solution[i]: 
            pattern[i] = 2
            solution_chars[i] = None
    # Yellows
    for i in range(5):
        if pattern[i] == 2:
            continue
        if guess[i] in solution_chars:
            pattern[i] = 1
            solution_chars.remove(guess[i]) # for doubles
    return tuple(pattern)

def get_pattern_counts(guess: str, possible_solutions: list[str]) -> dict[tuple[int], int]:
    pattern_counts: dict[tuple[int], int] = {}
    for sol in possible_solutions:
        pattern: tuple[int] = evaluate_guess(guess, sol)
        if pattern not in pattern_counts:
            pattern_counts[pattern] = 0
        pattern_counts[pattern] += 1
    return pattern_counts

def calculate_entropy(num_solutions: int, pattern_counts: dict[tuple[int], int]) -> float:
    entropy: float = 0.0
    for _, count in pattern_counts.items():
        probability: float = count / num_solutions
        info_bits: float = -log2(probability)
        entropy += probability * info_bits
    return entropy

def calculate_expected_remaining(num_solutions: int, pattern_counts: dict[tuple[int], int]) -> float:
    expected_remaining: float = 0
    for _, count in pattern_counts.items():
        probability: float = count / num_solutions
        # After seeing this pattern, we'd have 'count' solutions left
        expected_remaining += probability * count
    return expected_remaining

def get_score(guess: str, possible_solutions: list[str], known_letters: set[str], correct_positions: dict[int: str]) -> float:
    pattern_counts: dict[tuple[int], int] = get_pattern_counts(guess, possible_solutions)
    num_solutions: int = len(possible_solutions)
    # Calculate base entropy
    ent: float = calculate_entropy(num_solutions, pattern_counts)
    # Calculate expected remaining solutions after this guess
    expected_remaining: float = calculate_expected_remaining(num_solutions, pattern_counts)
    
    # Combine metrics (normalized)
    # Higher entropy = better, lower expected_remaining = better
    score: float = ent - (expected_remaining / num_solutions)
    
    # Bonus: prefer words that are actual solutions
    if (guess in possible_solutions
        and known_letters.issubset(set(guess))
        and all(guess[pos] == letter for pos, letter in correct_positions.items())):
        score += 0.5
    return score

class WordleSolver:
    def __init__(self, initial_guess: str = 'raise') -> None:
        self.possible_solutions: list[str] = load_words(POSSIBLE_SOLUTIONS_PATH)
        self.allowed: list[str] = load_words(ALLOWED_GUESSES_PATH)

        self.suggestion: str = initial_guess
        self.guessed: list[str] = [] # list of words we already guessed
        self.known_letters: set[str] = set() # set pf letters we know are in the solution
        self.correct_positions: dict[int, str] = {} # position : letter
    
    def process_feedback(self, pattern: tuple[int]) -> None:
        
        # Update remaining possible solutions
        self.possible_solutions = [sol for sol in self.possible_solutions if evaluate_guess(self.suggestion, sol) == pattern]
        
        # Update known informatioon
        self.guessed.append(self.suggestion)
        for i, (letter, color) in enumerate(zip(self.suggestion, pattern)):
            if color == 2:  # Green
                self.correct_positions[i] = letter
                self.known_letters.add(letter)
            elif color == 1:  # Yellow
                self.known_letters.add(letter)

        if len(self.possible_solutions) == 0:
            raise ValueError('Invalid feedback or word not present in database')

        # If we're down to very few solutions, just pick one
        elif len(self.possible_solutions) <= 2:
            self.suggestion = self.possible_solutions[0]
        # Otherwise, calculate the best next guess
        else:
            best_score: float = -float('inf')
            for word in self.allowed:
                if word in self.guessed: continue
                score: float = get_score(word, self.possible_solutions, self.known_letters, self.correct_positions)
                if score > best_score:
                    best_score = score
                    self.suggestion = word