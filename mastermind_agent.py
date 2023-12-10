import random


def generate_random_code():
    return [random.randint(1, 6) for _ in range(4)]


class Agent:
    def generate_next_code(self, state):
        return generate_random_code()
