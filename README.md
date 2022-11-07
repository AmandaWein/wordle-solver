# wordle-solver
A personal project to write a program that solves the daily game Wordle.

This project was created prior to the New York Times purchase of the game, and so the included word list is no longer accurate.

Guesses are determined based on the frequency with which each letter appears in each of the 5 possible positions within words in the word list.

To use the Wordle solver, first enter a guess in the game. Then, tell the solver what your guess was and what the results were for each letter (green, grey, or yellow). The solver will then suggest a word for your next guess while accounting for the results of all previous guesses.

According to this algorithm, the best starting guess is SLATE, followed by CRONY and HUMID.
