import random
import uuid


class MastermindGame:
    def __init__(self):
        self.game_id = str(uuid.uuid4())
        self.secret_code = [random.randint(1, 6) for _ in range(4)]
        self.attempts = 0

    def iteration(self, user_code):
        if user_code == self.secret_code:
            print("Congratulations! You have guessed the code.")
            return self.game_id, self.attempts, self.secret_code, user_code, 4, 4

        correct_position = sum(
            u == s for u, s in zip(user_code, self.secret_code))
        correct_digit = sum(min(user_code.count(
            digit), self.secret_code.count(digit)) for digit in set(user_code))
        print(f"{correct_position} correct digits in the correct position, {correct_digit - correct_position} correct digits in the incorrect position.")

        self.attempts += 1
        return self.game_id, self.attempts, self.secret_code, user_code, correct_position, correct_digit

    def play(self):
        while self.attempts < 10:
            user_code = [int(digit)
                         for digit in input("Enter a 4-digit code: ")]
            result = self.iteration(user_code)
            print(result)
            if result[4] == 4:
                exit()

        print("Sorry, you did not guess the code. The code was: ",
              ''.join(map(str, self.secret_code)))


game = MastermindGame()
game.play()
