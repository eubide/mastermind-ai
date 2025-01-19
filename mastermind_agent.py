from abc import ABC, abstractmethod
from typing import List, Set, Tuple, Optional
import random
from itertools import product
from dataclasses import dataclass


@dataclass
class GameFeedback:
    """Feedback from a game move"""
    correct_position: int
    correct_digit: int


class MastermindStrategy(ABC):
    """Abstract base class for Mastermind solving strategies"""

    @abstractmethod
    def generate_next_code(self, previous_moves: List[List]) -> List[int]:
        """Generate the next guess based on previous feedback.

        Args:
            previous_moves: List of previous moves and their feedback

        Returns:
            List[int]: Next guess
        """
        pass


class KnuthStrategy(MastermindStrategy):
    """Implementation of Knuth's five-guess algorithm"""

    def __init__(self):
        """Initialize the strategy with all possible codes."""
        self.possible_codes = list(product(range(1, 7), repeat=4))
        self.last_guess = None
        self.first_guess = True

    def _get_feedback(self, code: Tuple[int, ...], guess: Tuple[int, ...]) -> GameFeedback:
        """Calculate feedback for a guess against a code."""
        correct_pos = sum(c == g for c, g in zip(code, guess))

        # Count correct digits regardless of position
        code_counts = [code.count(i) for i in range(1, 7)]
        guess_counts = [guess.count(i) for i in range(1, 7)]
        correct_digits = sum(min(c, g) for c, g in zip(code_counts, guess_counts))

        return GameFeedback(correct_pos, correct_digits - correct_pos)

    def _is_consistent(
        self,
        code: Tuple[int, ...],
        guess: List[int],
        feedback: GameFeedback,
    ) -> bool:
        """Check if a code is consistent with the feedback from a guess."""
        move_feedback = self._get_feedback(code, tuple(guess))
        return (move_feedback.correct_position == feedback.correct_position and 
                move_feedback.correct_digit == feedback.correct_digit)

    def generate_next_code(self, previous_moves: List[List]) -> List[int]:
        if self.first_guess:
            # First guess is [1, 1, 2, 2] as it provides good information
            self.first_guess = False
            self.last_guess = [1, 1, 2, 2]
            return self.last_guess

        # Get the last non-empty state
        last_move = None
        for move in previous_moves:
            if move[0] != [0, 0, 0, 0]:
                last_move = move
                break

        if not last_move:
            return list(random.choice(self.possible_codes))

        # Filter possible codes based on the feedback
        feedback = GameFeedback(correct_position=last_move[1], correct_digit=last_move[2])
        
        self.possible_codes = [
            code
            for code in self.possible_codes
            if self._is_consistent(code, self.last_guess, feedback)
        ]

        if not self.possible_codes:
            # If no codes remain (shouldn't happen), reset
            self.possible_codes = list(product(range(1, 7), repeat=4))

        # Choose a random code from remaining possibilities
        next_guess = list(random.choice(self.possible_codes))
        self.last_guess = next_guess
        return next_guess


class RandomStrategy(MastermindStrategy):
    """Simple random guessing strategy"""

    def generate_next_code(self, previous_moves: List[List]) -> List[int]:
        """Generate a random code."""
        return [random.randint(1, 6) for _ in range(4)]


class SimpleStrategy(MastermindStrategy):
    """A simple strategy that tries to find one correct position at a time"""

    def __init__(self):
        self.current_position = 0
        self.found_positions = {}
        self.current_digit = 1

    def generate_next_code(self, previous_moves: List[List]) -> List[int]:
        # Get last move's feedback
        last_move = None
        for move in previous_moves:
            if move[0] != [0, 0, 0, 0]:
                last_move = move
                break

        if last_move:
            feedback = GameFeedback(correct_position=last_move[1], correct_digit=last_move[2])
            if feedback.correct_position > len(self.found_positions):
                # We found a correct position
                self.found_positions[self.current_position] = self.current_digit
                self.current_position += 1
                self.current_digit = 1
            else:
                # Try next digit for current position
                self.current_digit = (self.current_digit % 6) + 1

        # Generate next guess
        guess = [1] * 4  # Default values
        for pos, digit in self.found_positions.items():
            guess[pos] = digit
        if self.current_position < 4:
            guess[self.current_position] = self.current_digit

        return guess


class Agent:
    """An agent that plays the Mastermind game using a configurable strategy."""

    def __init__(self, strategy: Optional[MastermindStrategy] = None):
        """Initialize the agent with a strategy.
        
        Args:
            strategy: The strategy to use. Defaults to KnuthStrategy if None.
        """
        self.strategy = strategy or KnuthStrategy()

    def generate_next_code(self, state: List[List]) -> List[int]:
        """Generate the next guess using the current strategy."""
        return self.strategy.generate_next_code(state)
