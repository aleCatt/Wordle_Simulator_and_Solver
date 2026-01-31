'''
🧠 How to Use the Solver

```bash
python wordle_solver.py
```

1.  The solver will suggest a starting word (default: 'soare' or 'salet').
2.  Enter that word into your game.
3.  The solver will ask for feedback. Enter a 5-digit string representing the colors you received:
    *   0: Grey/Miss (Letter not in word)
    *   1: Yellow (Wrong position)
    *   2: Green (Correct position)
    
    Example:
        If the true word is ABACK and you guess CRANE:
        *   C is yellow (1)
        *   R is grey (0)
        *   A is green (2)
        *   N is grey (0)
        *   E is grey (0)

        You would type: `10200` into the solver.

4.  The solver will calculate the entropy of all valid words and suggest the next best guess.
'''

from wordle_utils import *

# Only possible solutions
with open(POSSIBLE_SOLUTIONS_PATH, 'r') as solutions_file:
    possible_solutions = [line.strip() for line in solutions_file]

# All allowed words
with open(ALLOWED_GUESSES_PATH, 'r') as allowed_file:
    allowed = [line.strip() for line in allowed_file]

# Track learned information
guessed = []  # Words we've already guessed
known_letters = set()  # Letters we know are in the word
correct_positions = {} # position -> letter

# Initial guess, good ones: 'soare', 'salet', 'trace'
best_word = 'raise'

print(f'Suggestion: {best_word}')

for turn in range(6):

    pattern = input('Write feedback: ')
    pattern = tuple(int(c) for c in pattern)
    if pattern == (2, 2, 2, 2, 2): 
        print("Solved!")
        break

    # Update learned information from the guess we just made
    guessed.append(best_word)
    for i, (letter, color) in enumerate(zip(best_word, pattern)):
        if color == 2:  # Green
            correct_positions[i] = letter
            known_letters.add(letter)
        elif color == 1:  # Yellow
            known_letters.add(letter)

    # Filter possible solutions based on feedback
    possible_solutions = filter_solutions(best_word, pattern, possible_solutions)

    print(f'Remaining solutions: {len(possible_solutions)}')
    
    # Check if we have no valid solutions left (likely a feedback error)
    if len(possible_solutions) == 0:
        print("⚠️  No valid solutions remaining! Please check your feedback patterns.")
        break
    
    # If we're down to very few solutions, just pick one
    if len(possible_solutions) <= 2:
        best_word = possible_solutions[0]
        print(f'Suggestion: {best_word}')
        continue

    # Otherwise, calculate the best next guess
    best_score = -1
    best_word = None

    for word in allowed:

        if word in guessed: continue

        # Calculate base entropy
        ent = calculate_entropy(word, possible_solutions)
        
        # Calculate expected remaining solutions after this guess
        expected_remaining = calculate_expected_remaining(word, possible_solutions)
        
        # Combine metrics (normalized)
        # Higher entropy = better, lower expected_remaining = better
        score = ent - (expected_remaining / len(possible_solutions))
        
        # Bonus: prefer words that are actual solutions
        if (word in possible_solutions
            and known_letters.issubset(set(word))
            and all(word[pos] == letter for pos, letter in correct_positions.items())):
            score += 0.5
        
        if score > best_score:
            best_score = score
            best_word = word

    print(f'Suggestion: {best_word}')
