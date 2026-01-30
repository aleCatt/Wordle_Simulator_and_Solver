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

with open(POSSIBLE_SOLUTIONS_PATH, 'r') as solutions_file:
    solution = random.choice(solutions_file.readlines()).strip()

# All allowed words
with open(ALLOWED_GUESSES_PATH, 'r') as allowed_file:
    allowed = [line.strip() for line in allowed_file]

def update_gamestate(guess: str, solution: str = solution) -> None:
    global gamestate

    color = evaluate_guess(guess, solution)

    for i in range(5):
        gamestate += COLORS[color[i]] + guess[i] + COLORS[-1]

    gamestate += '\n'

    return 1

gamestate = ''

for guess in range(6):
    
    new_guess = input('Guess: ').lower()

    while new_guess not in allowed: 
        print('Not valid')
        new_guess = input('Guess: ').lower()

    update_gamestate(new_guess)
    print(gamestate)

    if new_guess == solution:
        break

print(f'The word was: {COLORS[2]}{solution}')
