import random
import uuid
import random
import os


def generate_code():
    return [random.randint(1, 6) for _ in range(4)]


class Agent:
    def generate_code(self):
        return generate_code()


class MastermindGame:
    def __init__(self):
        self.game_id = str(uuid.uuid4())
        self.secret_code = generate_code()
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
        directory = "games"
        if not os.path.exists(directory):
            os.makedirs(directory)
        filepath = os.path.join(directory, self.game_id+".txt")

        my_agent = Agent()
        with open(filepath, "a") as file:
            while self.attempts < 10:
                user_code = my_agent.generate_code()
                result = self.iteration(user_code)
                # print(*result, sep=", ")
                file.write(", ".join(map(str, result[3:6])) + "\n")
                if result[4] == 4:
                    # print("Congratulations! You have guessed the code")
                    file.write('OK' + str(result[2]))
                    exit()

            # print("Sorry, you did not guess the code. The code was: ",
            #       ''.join(map(str, self.secret_code)))
            file.write('KO' + str(result[2]))

        # if it's KO then delete the file
        if result[4] != 4:
            os.remove(filepath)


game = MastermindGame()
game.play()
