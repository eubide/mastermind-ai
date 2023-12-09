import random
import uuid
import random
import os
from mastermind_agent import Agent


def generate_code():
    return [random.randint(1, 6) for _ in range(4)]


class Mastermind:
    def __init__(self):
        self.MAX_ATTEMPTS = 10
        self.game_id = str(uuid.uuid4())
        self.secret_code = generate_code()
        self.attempts = 0
        self.movements = []
        self.guessed = False

    def evalue_user_code(self, user_code):
        if user_code == self.secret_code:
            return self.game_id, self.attempts, self.secret_code, user_code, 4, 4

        correct_position = sum(
            u == s for u, s in zip(user_code, self.secret_code))
        correct_digit = sum(min(user_code.count(
            digit), self.secret_code.count(digit)) for digit in set(user_code))

        self.attempts += 1
        return self.game_id, self.attempts, self.secret_code, user_code, correct_position, correct_digit

    def print_game(self):
        if self.guessed == 4 and self.attempts > 3:
            print(f"You win in {self.attempts}!")
            directory = "games"
            if not os.path.exists(directory):
                os.makedirs(directory)
            filepath = os.path.join(directory, self.game_id+".txt")
            with open(filepath, "w") as f:
                for movement in self.movements:
                    f.write(str(movement)+"\n")

    def game(self):
        my_agent = Agent()

        while True:
            user_code = my_agent.generate_code()
            result = self.evalue_user_code(user_code)
            self.movements.append(result)
            self.guessed = result[4]

            if self.guessed == 4 or self.attempts == self.MAX_ATTEMPTS:
                self.print_game()
                return


game = Mastermind()
game.game()
