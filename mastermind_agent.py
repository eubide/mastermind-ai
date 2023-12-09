import random


def generate_code():
    return [random.randint(1, 6) for _ in range(4)]


class Agent:
    def generate_code(self):
        return generate_code()
