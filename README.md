# Wordle Simulator & Entropy Solver

## 📂 Project Structure

*   **`wordle_simulator.py`**: A fully playable version of Wordle that runs in your terminal with colored output.
*   **`wordle_solver.py`**: An AI assistant that suggests the mathematically optimal next guess based on your current feedback.
*   **`wordle_utils.py`**: Shared logic for game mechanics, pattern evaluation, and entropy calculation.
*   **`wordle_solutions.txt`**: A list of possible target words (the "answer key").
*   **`wordle_allowed_guesses.txt`**: A comprehensive list of all valid 5-letter words accepted as guesses.

### Setup
Ensure all `.py` and `.txt` files are in the same directory.

## ℹ️ How the Solver Works

The solver utilizes **Information Theory** (specifically Shannon Entropy) to maximize the information gained from every guess.

1.  **Filtering**: It takes the current list of possible solutions and removes any that do not match the feedback received so far.
2.  **Entropy Calculation**: For every allowed guess, it calculates how much that guess would narrow down the remaining possibilities on average.
    *   $E[I] = \sum_{p} P(p) \cdot \log_2(\frac{1}{P(p)})$
3.  **Selection**: It suggests the word with the highest Entropy score. If a word is a potential solution *and* has high entropy, it is prioritized.
