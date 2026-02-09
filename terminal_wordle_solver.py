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

from wordle_utils import (load_words, filter_solutions, get_score,
                          POSSIBLE_SOLUTIONS_PATH, ALLOWED_GUESSES_PATH)

def get_pattern() -> tuple[int]:
    pattern_string = input('Write feedback (0: gray, 1: yellow, 2: green): ')
    while not (all(char in '012' for char in pattern_string) and len(pattern_string) == 5):
        print('Invalid format.')
        pattern_string = input('Write feedback (0: gray, 1: yellow, 2: green): ')
    return tuple(int(c) for c in pattern_string)

def get_suggestion(suggestion: str, pattern: tuple[int]) -> str:
    global guessed, correct_positions, known_letters, possible_solutions, allowed
    
    # Update learned information from the guess we just made
    guessed.append(suggestion)
    for i, (letter, color) in enumerate(zip(suggestion, pattern)):
        if color == 2:  # Green
            correct_positions[i] = letter
            known_letters.add(letter)
        elif color == 1:  # Yellow
            known_letters.add(letter)

    # Filter possible solutions based on feedback
    possible_solutions = filter_solutions(suggestion, pattern, possible_solutions)
    print(f'Remaining solutions: {len(possible_solutions)}')

    suggestion: str = ''
    # Check if we have no valid solutions left (likely a feedback error)
    if len(possible_solutions) == 0:
        print('No valid solutions remaining! Please check your feedback patterns.')
    # If we're down to very few solutions, just pick one
    elif len(possible_solutions) <= 2:
        suggestion = possible_solutions[0]
    # Otherwise, calculate the best next guess
    else:
        best_score: float = -float('inf')
        for word in allowed:
            if word in guessed: continue
            score: float = get_score(word, possible_solutions, known_letters, correct_positions)
            if score > best_score:
                best_score = score
                suggestion = word
    return suggestion

if __name__ == '__main__':
    # Only possible solutions
    possible_solutions: list[str] = load_words(POSSIBLE_SOLUTIONS_PATH)
    # All allowed words
    allowed: list[str] = load_words(ALLOWED_GUESSES_PATH)

    # Track learned information
    guessed: list[str] = []  # Words we've already guessed
    known_letters: set[str] = set()  # Letters we know are in the word
    correct_positions: dict[int, str] = {} # position: letter

    # Initial guess, good ones: 'soare', 'salet', 'trace'
    suggestion: str = 'raise'

    for _ in range(5):
        print(suggestion)
        pattern = get_pattern()
        if pattern == (2, 2, 2, 2, 2): 
            print("Solved!")
            break
        suggestion = get_suggestion(suggestion, pattern)