# Wordle Simulator & Solver

## 📂 Project Structure

*   **`wordle_simulator.py`**: A fully playable Wordle game that runs in your terminal with colored output.
*   **`wordle_solver.py`**: A script assistant that calculates the optimal next guess.
*   **`wordle_utils.py`**: Shared logic for pattern matching, entropy calculation, and scoring.
*   **`wordle_solutions.txt`**: A list of possible target words.
*   **`wordle_allowed_guesses.txt`**: A comprehensive list of all valid 5-letter inputs.

### Setup
Ensure all `.py` and `.txt` files are in the same directory.

## ℹ️ How the Solver Works

The solver uses a **Hybrid Scoring System** ($Score$) that balances information gathering with the likelihood of winning.

1.  **Filtering**: It eliminates any words from the solution pool that do not match the feedback (Green/Yellow/Gray) received so far.
2.  **Information Calculation**: It calculates **Shannon Entropy** ($E$) to measure how well a guess splits the remaining possibilities.
3.  **Optimization**:
    *   **Group Reduction**: It penalizes words that are expected to leave a large number of remaining candidates.
    *   **Solution Bonus**: It adds a score boost ($+0.5$) if the guess is a **valid potential answer** that fits the current known letters.
    
    $$Score = Entropy - NormalizedRemaining + Bonus$$
