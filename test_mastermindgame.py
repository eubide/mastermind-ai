from automata import Automata
import pytest
from mastermindgame import Mastermind, Agent
import uuid


def test_game_id_is_uuid():
    game = Mastermind()
    # This will raise an exception if game_id is not a valid UUID
    uuid.UUID(game.game_id, version=4)


def test_secret_code_has_4_digits():
    game = Mastermind()
    assert len(game.secret_code) == 4


def test_attempts_increment():
    game = Mastermind()
    assert game.attempts == 0
    game.evalue_user_code([1, 1, 1, 1])
    assert game.attempts == 1


def test_iteration_returns_correct_results():
    game = Mastermind()
    game.secret_code = [1, 2, 3, 4]
    result = game.evalue_user_code([1, 2, 3, 4])
    assert result == (game.game_id, 1, [1, 2, 3, 4], [1, 2, 3, 4], 4)


def test_play():
    game = Mastermind()
    game.secret_code = [1, 2, 3, 4]
    with pytest.raises(SystemExit):
        game.game()


def test_generate_code_returns_4_digits():
    automata = Agent()
    code = automata.generate_code()
    assert len(code) == 4


def test_generate_code_returns_numbers_from_1_to_6():
    automata = Agent()
    code = automata.generate_code()
    for digit in code:
        assert 1 <= digit <= 6


def test_generate_code_returns_different_codes():
    automata = Agent()
    code1 = automata.generate_code()
    code2 = automata.generate_code()
    assert code1 != code2
