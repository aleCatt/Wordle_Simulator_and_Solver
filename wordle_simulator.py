'''
🎮 How to Play


```bash
python wordle_simulator.py
```

1.  Type a 5-letter guess and press Enter.
2.  The terminal will display your guess with color codes:
    *   Green: Correct letter in the correct spot.
    *   Yellow: Correct letter, but in the wrong spot.
    *   Purple: Letter is not in the word. (Contrasts better with yellow)
3.  You have 6 attempts to guess the word.
'''

import random
from wordle_utils import *

def update_gamestate(gamestate: str, guess: str, pattern: list[int]) -> str:
    for i in range(5):
        gamestate += COLORS[pattern[i]] + guess[i] + COLORS[-1]
    return gamestate + '\n'

def display_keyboard(letters: dict[str, int]) -> None:
    rows: list[str] = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm']
    for i, row in enumerate(rows):
        for letter in row:
            print(f'{COLORS[letters[letter]]}{letter}{COLORS[-1]} ', end='')
        print('\n' + ' ' * (i+1), end='')
    print()

def main() -> None:
    solution: str = random.choice(load_words(POSSIBLE_SOLUTIONS_PATH))
    # All allowed words
    allowed: list[str] = load_words(ALLOWED_GUESSES_PATH)
    gamestate: str = ''
    letters: dict[str, int] = {chr(i): -1 for i in range(ord('a'), ord('z') + 1)}

    for guess in range(6):
        new_guess: str = input('Guess: ').lower()
        while new_guess not in allowed: 
            print('Not valid')
            new_guess: str = input('Guess: ').lower()

        pattern: tuple[int] = evaluate_guess(new_guess, solution)
        for i in range(5):
            letters[new_guess[i]] = max(letters[new_guess[i]], pattern[i])

        gamestate: str = update_gamestate(gamestate, new_guess, pattern)
        print(gamestate)
        display_keyboard(letters)

        if new_guess == solution:
            break

    print(f'The word was: {COLORS[2]}{solution}{COLORS[-1]}')

if __name__ == '__main__':
    main()