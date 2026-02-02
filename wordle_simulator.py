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

def update_gamestate(gamestate: str, guess: str, solution: str) -> str:
    color: list[int] = evaluate_guess(guess, solution)
    for i in range(5):
        gamestate += COLORS[color[i]] + guess[i] + COLORS[-1]
    return gamestate + '\n'

def main() -> None:
    solution: str = random.choice(load_words(POSSIBLE_SOLUTIONS_PATH))
    # All allowed words
    allowed: list[str] = load_words(ALLOWED_GUESSES_PATH)
    gamestate: str = ''

    for guess in range(6):
        new_guess: str = input('Guess: ').lower()
        while new_guess not in allowed: 
            print('Not valid')
            new_guess: str = input('Guess: ').lower()

        gamestate = update_gamestate(gamestate, new_guess, solution)
        print(gamestate)

        if new_guess == solution:
            break

    print(f'The word was: {COLORS[2]}{solution}{COLORS[-1]}')

if __name__ == '__main__':
    main()