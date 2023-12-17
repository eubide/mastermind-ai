import pytest
from mastermind_env import Mastermind


@pytest.fixture
def game():
    game = Mastermind()
    game.secret_code = [1, 2, 3, 4]
    game.win = False
    game.attempts = 0
    return game


def test_evalue_user_code_give_a_code_none_is_well_positioned(game):
    assert game.evalue_user_code([2, 3, 4, 1]) == (
        game.game_id, game.attempts, game.secret_code, [2, 3, 4, 1], 0, 4)


def test_mastermind_game(game):
    assert game.win == False
    assert game.attempts == 0

    # Test the initial state of the game
    assert game.state == [[[0, 0, 0, 0], 0, 0]] * game.MAX_ATTEMPTS

    # Test the evaluation of user code
    assert game.evalue_user_code([1, 2, 3, 4]) == (
        game.game_id, game.attempts, game.secret_code, [1, 2, 3, 4], 4, 0)

    # Test the evaluation of user code
    assert game.evalue_user_code([1, 2, 4, 5]) == (
        game.game_id, game.attempts, game.secret_code, [1, 2, 4, 5], 2, 1)

    # Test adding movement to state
    game.add_movement_to_state([1, 2, 3, 4], 2, 2)
    assert game.state[game.attempts] == [[1, 2, 3, 4], 2, 2]

    # Test the game loop
    game.game()
    assert game.win == True or game.attempts == game.MAX_ATTEMPTS

    # Test printing the state
    game.print_state(debug=True)
