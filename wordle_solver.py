from wordle_utils import *

# Only possible solutions
with open(POSSIBLE_SOLUTIONS_PATH, 'r') as solutions_file:
    possible_solutions = [line.strip() for line in solutions_file]

# All allowed words
with open(ALLOWED_GUESSES_PATH, 'r') as allowed_file:
    allowed = [line.strip() for line in allowed_file]

# Initial guess, try also 'salet', 'trace'
best_word = 'soare'
print(f'Suggestion: {best_word}')

for _ in range(6):

    pattern = input('Write feedback: ')
    pattern = tuple(int(c) for c in pattern)
    if pattern == (2, 2, 2, 2, 2): 
        break

    possible_solutions = filter_solutions(best_word, pattern, possible_solutions)

    best_entropy = -1
    best_word = None

    for word in allowed:
        ent = calculate_entropy(word, possible_solutions)

        if word in possible_solutions:
            ent += 1e-5 # Break ties in favor of possible solutions

        if ent > best_entropy:
            best_entropy = ent
            best_word = word

    print(f'Suggestion: {best_word}')
