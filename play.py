from mastermind_env import Mastermind
from tqdm import tqdm

for _ in tqdm(range(100)):
    # Your code here
    game = Mastermind()
    game.game()
