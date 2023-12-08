from mastermindgame import MastermindGame
from tqdm import tqdm

for _ in tqdm(range(1000000)):
    # Your code here
    game = MastermindGame()
    game.play()
