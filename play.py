from mastermind_env import Mastermind
from tqdm import tqdm

for _ in tqdm(range(1000)):
    # Your code here
    game = Mastermind()
    game.game()
