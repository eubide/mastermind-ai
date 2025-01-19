from typing import List, Dict
from mastermind_env import Mastermind
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np


def run_games(num_games: int = 1000) -> List[Dict]:
    """Run multiple Mastermind games and collect statistics.

    Args:
        num_games: Number of games to run

    Returns:
        List[Dict]: Statistics for each game
    """
    stats = []

    for _ in tqdm(range(num_games), desc="Playing games"):
        game = Mastermind()
        won = game.game()

        stats.append(
            {"won": won, "attempts": game.state.attempts, "game_id": game.game_id}
        )

    return stats


def analyze_results(stats: List[Dict]) -> None:
    """Analyze and visualize game statistics.

    Args:
        stats: List of game statistics
    """
    wins = sum(1 for s in stats if s["won"])
    total = len(stats)
    win_rate = (wins / total) * 100

    # Calculate attempt distribution for wins
    attempts = [s["attempts"] for s in stats if s["won"]]
    avg_attempts = np.mean(attempts) if attempts else 0

    print(f"\nResults:")
    print(f"Total games: {total}")
    print(f"Wins: {wins} ({win_rate:.1f}%)")
    print(f"Average attempts for wins: {avg_attempts:.1f}")

    # Plot attempt distribution
    if attempts:
        plt.figure(figsize=(10, 6))
        plt.hist(attempts, bins=range(1, 12), align="left", rwidth=0.8)
        plt.title("Distribution of Attempts for Winning Games")
        plt.xlabel("Number of Attempts")
        plt.ylabel("Frequency")
        plt.grid(True, alpha=0.3)
        plt.savefig("attempt_distribution.png")
        plt.close()


if __name__ == "__main__":
    # Run games and analyze results
    stats = run_games(1000)
    analyze_results(stats)
