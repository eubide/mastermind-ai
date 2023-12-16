import random
import uuid
import random
import os
from mastermind_agent import Agent

# random.seed(0)


def generate_random_code():
    return [random.randint(1, 6) for _ in range(4)]


def flatten_list(nested_list):
    flat_list = []
    for element in nested_list:
        if isinstance(element, list):
            flat_list.extend(element)
        else:
            flat_list.append(element)
    return flat_list


class Mastermind:
    def __init__(self):

        self.DIRECTORY = "games"

        self.MAX_ATTEMPTS = 10
        self.game_id = str(uuid.uuid4())
        self.secret_code = generate_random_code()
        self.attempts = 0
        self.win = False
        self.state = [[[0, 0, 0, 0], 0, 0]
                      for _ in range(self.MAX_ATTEMPTS)]

    def print_state(self, debug=False):
        if self.win:

            if not os.path.exists(self.DIRECTORY):
                os.makedirs(self.DIRECTORY)
            filepath = os.path.join(self.DIRECTORY, self.game_id+".txt")
            with open(filepath, "w") as f:
                for row in self.state:
                    flat_row = flatten_list(row)
                    numbers_str = ', '.join(map(str, flat_row))
                    f.write(str(numbers_str)+"\n")

        if debug:
            if self.win:
                print(f"You win! in {self.attempts} attempts")
            else:
                print("You lose!")
                print(f"Secret code: {self.secret_code}")
            for row in self.state:
                flat_row = flatten_list(row)
                print(flat_row)

    def add_movement_to_state(self, user_code, correct_position, correct_digit):
        self.state[self.attempts] = [
            user_code, correct_position, correct_digit]

    def evalue_user_code(self, user_code):
        if user_code == self.secret_code:
            return self.game_id, self.attempts, self.secret_code, user_code, 4, 4

        correct_position = sum(
            u == s for u, s in zip(user_code, self.secret_code))
        correct_digit = sum(min(user_code.count(
            digit), self.secret_code.count(digit)) for digit in set(user_code))

        if correct_position == 4:
            self.win = True
        return self.game_id, self.attempts, self.secret_code, user_code, correct_position, correct_digit

    def game(self):
        my_agent = Agent()

        while True:
            user_code = my_agent.generate_next_code(self.state)
            result = self.evalue_user_code(user_code)
            self.add_movement_to_state(user_code, result[4], result[5])

            self.attempts += 1

            if self.win or self.attempts == self.MAX_ATTEMPTS:
                self.print_state(debug=True)
                return self.win


game = Mastermind()
game.game()
