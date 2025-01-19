from typing import List, Set, Tuple
import random
from itertools import product


class Agent:
    """An agent that plays the Mastermind game using a strategy."""

    def __init__(self):
        """Initialize the agent with all possible codes."""
        self.possible_codes = list(product(range(1, 7), repeat=4))
        self.last_guess = None
        self.first_guess = True

    def _get_feedback(
        self, code: Tuple[int, ...], guess: Tuple[int, ...]
    ) -> Tuple[int, int]:
        """Calculate feedback for a guess against a code.

        Args:
            code: The code to compare against
            guess: The guess to evaluate

        Returns:
            Tuple[int, int]: (correct positions, correct digits in wrong positions)
        """
        correct_pos = sum(c == g for c, g in zip(code, guess))

        # Count correct digits regardless of position
        code_counts = [code.count(i) for i in range(1, 7)]
        guess_counts = [guess.count(i) for i in range(1, 7)]
        correct_digits = sum(min(c, g) for c, g in zip(code_counts, guess_counts))

        return correct_pos, correct_digits - correct_pos

    def _is_consistent(
        self,
        code: Tuple[int, ...],
        guess: List[int],
        correct_pos: int,
        correct_digits: int,
    ) -> bool:
        """Check if a code is consistent with the feedback from a guess.

        Args:
            code: Code to check
            guess: Previous guess
            correct_pos: Number of correct positions from feedback
            correct_digits: Number of correct digits in wrong positions from feedback

        Returns:
            bool: True if the code is consistent with the feedback
        """
        feedback = self._get_feedback(code, tuple(guess))
        return feedback == (correct_pos, correct_digits)

    def generate_next_code(self, state: List[List]) -> List[int]:
        """Generate the next guess based on previous feedback.

        Args:
            state: Game state containing previous guesses and feedback

        Returns:
            List[int]: Next guess
        """
        if self.first_guess:
            # First guess is [1, 1, 2, 2] as it provides good information
            self.first_guess = False
            self.last_guess = [1, 1, 2, 2]
            return self.last_guess

        # Get the last non-empty state
        last_move = None
        for move in state:
            if move[0] != [0, 0, 0, 0]:
                last_move = move
                break

        if not last_move:
            return list(random.choice(self.possible_codes))

        # Filter possible codes based on the feedback
        guess = tuple(self.last_guess)
        correct_pos = last_move[1]
        correct_digits = last_move[2]

        self.possible_codes = [
            code
            for code in self.possible_codes
            if self._is_consistent(code, self.last_guess, correct_pos, correct_digits)
        ]

        if not self.possible_codes:
            # If no codes remain (shouldn't happen), reset
            self.possible_codes = list(product(range(1, 7), repeat=4))

        # Choose a random code from remaining possibilities
        next_guess = list(random.choice(self.possible_codes))
        self.last_guess = next_guess
        return next_guess
