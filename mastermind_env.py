from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional
import random
import uuid
import os
from datetime import datetime
from mastermind_agent import Agent, KnuthStrategy, RandomStrategy, SimpleStrategy


@dataclass
class GameState:
    """Class to represent the game state"""

    attempts: int
    max_attempts: int
    secret_code: List[int]
    moves: List[List]
    win: bool = False


@dataclass
class Feedback:
    """Class to represent move feedback"""

    correct_position: int
    correct_digit: int


class GameInterface(ABC):
    @abstractmethod
    def make_move(self, code: List[int]) -> Feedback:
        pass

    @abstractmethod
    def is_game_over(self) -> bool:
        pass


class GamePersistence:
    """Class to handle game state persistence"""

    def __init__(self, directory: str = "games"):
        self.directory = directory
        if not os.path.exists(directory):
            os.makedirs(directory)

    def save_game(self, game_id: str, state: GameState) -> None:
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        filepath = os.path.join(self.directory, f"{timestamp}_{game_id}.txt")
        try:
            with open(filepath, "w") as f:
                for move in state.moves:
                    flat_move = self._flatten_list(move)
                    f.write(f"{' | '.join(map(str, flat_move))}\n")
                f.write(" | ".join(map(str, state.secret_code)))
        except IOError as e:
            print(f"Error saving game state: {e}")

    @staticmethod
    def _flatten_list(nested_list: List) -> List:
        flat_list = []
        for element in nested_list:
            if isinstance(element, list):
                flat_list.extend(element)
            else:
                flat_list.append(element)
        return flat_list


class Mastermind(GameInterface):
    """A class representing the Mastermind game environment."""

    CODE_LENGTH = 4
    MIN_DIGIT = 1
    MAX_DIGIT = 6

    def __init__(self, max_attempts: int = 10):
        self.game_id = str(uuid.uuid4())
        self.state = GameState(
            attempts=0,
            max_attempts=max_attempts,
            secret_code=self._generate_random_code(),
            moves=[[0, 0, 0, 0] for _ in range(max_attempts)],
        )
        self.persistence = GamePersistence()

    @staticmethod
    def _generate_random_code() -> List[int]:
        """Generate a random code allowing repeated digits"""
        return [
            random.randint(Mastermind.MIN_DIGIT, Mastermind.MAX_DIGIT)
            for _ in range(Mastermind.CODE_LENGTH)
        ]

    def _validate_move(self, code: List[int]) -> None:
        """Validate a move before processing it"""
        if self.is_game_over():
            raise ValueError("Game is over")

        if len(code) != self.CODE_LENGTH:
            raise ValueError("Guess must be 4 digits long")

        if not all(isinstance(x, int) for x in code):
            raise ValueError("All digits must be integers")

        if not all(self.MIN_DIGIT <= x <= self.MAX_DIGIT for x in code):
            raise ValueError("Digits must be between 1 and 6")

    def make_move(self, code: List[int]) -> Feedback:
        """Make a move and get feedback"""
        self._validate_move(code)

        # Calculate correct positions
        correct_pos = sum(c == g for c, g in zip(self.state.secret_code, code))

        # Calculate correct digits (including those in correct position)
        code_counts = [code.count(i) for i in range(self.MIN_DIGIT, self.MAX_DIGIT + 1)]
        secret_counts = [
            self.state.secret_code.count(i)
            for i in range(self.MIN_DIGIT, self.MAX_DIGIT + 1)
        ]
        total_correct = sum(min(c, g) for c, g in zip(code_counts, secret_counts))

        # Correct digits but wrong position = total correct - correct positions
        feedback = Feedback(correct_pos, total_correct - correct_pos)
        self._update_state(code, feedback)
        return feedback

    def _update_state(self, code: List[int], feedback: Feedback) -> None:
        self.state.moves[self.state.attempts] = [
            code,
            feedback.correct_position,
            feedback.correct_digit,
        ]
        self.state.attempts += 1

        if feedback.correct_position == 4:
            self.state.win = True
            self.persistence.save_game(self.game_id, self.state)

    def is_game_over(self) -> bool:
        return self.state.win or self.state.attempts >= self.state.max_attempts

    def print_state(self, debug: bool = False) -> None:
        """Print the current game state.

        Args:
            debug: If True, prints detailed game information
        """
        if self.state.win or debug:
            self.persistence.save_game(self.game_id, self.state)

        if debug:
            if self.state.win:
                print(f"You win! in {self.state.attempts} attempts")
            else:
                print("You lose!")
                print(f"Secret code: {self.state.secret_code}")
            for move in self.state.moves:
                flat_move = self.persistence._flatten_list(move)
                print(flat_move)

    def game(self, strategy_name: str = "knuth") -> bool:
        """Run the game loop.

        Args:
            strategy_name: The name of the strategy to use. Options are:
                - "knuth": Knuth's five-guess algorithm (default)
                - "random": Random guessing strategy
                - "simple": Simple position-by-position strategy

        Returns:
            bool: True if the player won, False otherwise
        """
        # Create the agent with the selected strategy
        strategy_map = {
            "knuth": None,  # None will use the default KnuthStrategy
            "random": RandomStrategy(),
            "simple": SimpleStrategy()
        }

        if strategy_name not in strategy_map:
            raise ValueError(f"Invalid strategy name. Options are: {list(strategy_map.keys())}")

        my_agent = Agent(strategy=strategy_map[strategy_name])

        while not self.is_game_over():
            try:
                user_code = my_agent.generate_next_code(self.state.moves)
                result = self.make_move(user_code)
            except Exception as e:
                print(f"Error during game play: {e}")
                break

        self.print_state(debug=False)
        return self.state.win


if __name__ == "__main__":
    # Example of running the game with different strategies
    strategies = ["knuth", "random", "simple"]
    results = {}

    for strategy in strategies:
        game = Mastermind()
        won = game.game(strategy)
        results[strategy] = {
            "won": won,
            "attempts": game.state.attempts
        }

    # Print results
    print("\nResults for different strategies:")
    for strategy, result in results.items():
        status = "Won" if result["won"] else "Lost"
        print(f"{strategy.capitalize()}: {status} in {result['attempts']} attempts")
