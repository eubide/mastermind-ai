import random
import uuid
import random


class Automata:
    def generate_code(self):
        return [random.randint(1, 6) for _ in range(4)]


class MastermindGame:
    def __init__(self):
        self.game_id = str(uuid.uuid4())
        self.secret_code = [random.randint(1, 6) for _ in range(4)]
        self.attempts = 0

    def iteration(self, user_code):
        if user_code == self.secret_code:
            return self.game_id, self.attempts, self.secret_code, user_code, 4, 4

        correct_position = sum(
            u == s for u, s in zip(user_code, self.secret_code))
        correct_digit = sum(min(user_code.count(
            digit), self.secret_code.count(digit)) for digit in set(user_code))

        self.attempts += 1
        return self.game_id, self.attempts, self.secret_code, user_code, correct_position, correct_digit

    def play(self):
        automata = Automata()
        while self.attempts < 100:
            user_code = automata.generate_code()
            result = self.iteration(user_code)
            print(result)
            if result[4] == 4:
                print("Congratulations! You have guessed the code.")
                exit()

        print("Sorry, you did not guess the code. The code was: ",
              ''.join(map(str, self.secret_code)))


game = MastermindGame()
game.play()
