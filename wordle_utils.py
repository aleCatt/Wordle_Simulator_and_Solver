from math import log2

POSSIBLE_SOLUTIONS_PATH = 'wordle_solutions.txt'
ALLOWED_GUESSES_PATH = 'wordle_allowed_guesses.txt'

COLORS = {
    0 : '\033[95m', # Purple (Contrasts well with yellow)
    2 : '\033[92m', # Green
    1 : '\033[93m', # Yellow
    -1 : '\033[0m'  # RESET
}

def evaluate_guess(guess: str, solution: str) -> list[int]:

    solution_chars = list(solution)
    pattern = [0] * 5

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

def filter_solutions(guess: str, pattern: list[int], possible_solutions: list[str]) -> list[str]:
    return [sol for sol in possible_solutions if evaluate_guess(guess, sol) == pattern]

def calculate_entropy(guess: str, possible_solutions: list[str]) -> float:

    pattern_counts = {}

    for sol in possible_solutions:
        pattern = evaluate_guess(guess, sol)
        if pattern not in pattern_counts:
            pattern_counts[pattern] = 0
        pattern_counts[pattern] += 1
    
    entropy = 0
    num_solutions = len(possible_solutions)

    for pattern, count in pattern_counts.items():
        probability = count / num_solutions
        info_bits = -log2(probability)

        entropy += probability * info_bits

    return entropy