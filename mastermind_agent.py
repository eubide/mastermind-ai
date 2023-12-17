import random


def generate_random_code():
    return random.sample(range(1, 7), 4)


class Agent:
    def generate_next_code(self, state):
        return generate_random_code()
