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

from wordle_utils import WordleSolver
        
def get_pattern() -> tuple[int]:
    pattern_string = input('Write feedback (0: gray, 1: yellow, 2: green): ')
    while not (all(char in '012' for char in pattern_string) and len(pattern_string) == 5):
        print('Invalid format.')
        pattern_string = input('Write feedback (0: gray, 1: yellow, 2: green): ')
    return tuple(int(c) for c in pattern_string)

def main() -> None:
    solver = WordleSolver()
    for _ in range(5):
        print(f'Suggestion: {solver.suggestion.upper()}')
        pattern = get_pattern()
        if pattern == (2, 2, 2, 2, 2): 
            print("Solved!")
            break
        solver.process_feedback(pattern)

if __name__ == '__main__':
    main()