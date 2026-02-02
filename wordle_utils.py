from math import log2

POSSIBLE_SOLUTIONS_PATH: str = 'wordle_solutions.txt'
ALLOWED_GUESSES_PATH: str = 'wordle_allowed_guesses.txt'

COLORS: dict[int, str] = {
    0 : '\033[95m', # Purple (Contrasts well with yellow)
    2 : '\033[92m', # Green
    1 : '\033[93m', # Yellow
    -1 : '\033[0m'  # RESET
}

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

def filter_solutions(guess: str, pattern: tuple[int], possible_solutions: list[str]) -> list[str]:
    return [sol for sol in possible_solutions if evaluate_guess(guess, sol) == pattern]

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
