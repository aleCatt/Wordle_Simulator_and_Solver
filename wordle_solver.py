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

def main() -> None:
    # Only possible solutions
    possible_solutions: list[str] = load_words(POSSIBLE_SOLUTIONS_PATH)
    # All allowed words
    allowed: list[str] = load_words(ALLOWED_GUESSES_PATH)

    # Track learned information
    guessed: list[str] = []  # Words we've already guessed
    known_letters: set[str] = set()  # Letters we know are in the word
    correct_positions: dict[int, str] = {} # position: letter

    # Initial guess, good ones: 'soare', 'salet', 'trace'
    best_word: str = 'raise'

    print(f'Suggestion: {best_word}')

    for turn in range(6):

        pattern: tuple[int] = tuple(int(c) for c in input('Write feedback: '))
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
            print("No valid solutions remaining! Please check your feedback patterns.")
            break
        
        # If we're down to very few solutions, just pick one
        if len(possible_solutions) <= 2:
            best_word = possible_solutions[0]
            print(f'Suggestion: {best_word}')
            continue

        # Otherwise, calculate the best next guess
        best_score: float = -1.0
        best_word: str = None

        for word in allowed:

            if word in guessed: continue

            score: float = get_score(word, possible_solutions, known_letters, correct_positions)
            
            if score > best_score:
                best_score = score
                best_word = word

        print(f'Suggestion: {best_word}')

if __name__ == '__main__':
    main()