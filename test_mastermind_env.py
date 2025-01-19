import pytest
from mastermind_env import Mastermind, GameState, Feedback


@pytest.fixture
def game():
    game = Mastermind()
    game.state.secret_code = [1, 2, 3, 4]
    game.state.attempts = 0
    return game


def test_initial_game_state(game):
    """Test that the game initializes with correct state"""
    assert game.state.attempts == 0
    assert len(game.state.moves) == game.state.max_attempts
    assert all(move == [0, 0, 0, 0] for move in game.state.moves)


def test_make_move_all_correct(game):
    """Test feedback when all digits are in correct position"""
    feedback = game.make_move([1, 2, 3, 4])
    assert feedback == Feedback(correct_position=4, correct_digit=0)
    assert game.state.moves[0] == [[1, 2, 3, 4], 4, 0]


def test_make_move_none_well_positioned(game):
    """Test feedback when no digits are in correct position"""
    feedback = game.make_move([2, 3, 4, 1])
    assert feedback == Feedback(correct_position=0, correct_digit=4)
    assert game.state.moves[0] == [[2, 3, 4, 1], 0, 4]


def test_make_move_mixed_match(game):
    """Test feedback when some digits are correct and some in wrong positions"""
    feedback = game.make_move([1, 2, 4, 5])
    assert feedback == Feedback(correct_position=2, correct_digit=1)
    assert game.state.moves[0] == [[1, 2, 4, 5], 2, 1]


def test_game_state_updates_after_move(game):
    """Test that game state properly updates after making moves"""
    initial_attempts = game.state.attempts
    game.make_move([1, 2, 3, 4])
    assert game.state.attempts == initial_attempts + 1
    assert game.state.moves[0] != [0, 0, 0, 0]


def test_game_over_conditions(game):
    """Test different game over conditions"""
    # Game not over at start
    assert not game.is_game_over()

    # Game over on perfect match
    game.make_move([1, 2, 3, 4])
    assert game.is_game_over()

    # Game over on max attempts
    game = Mastermind(max_attempts=1)
    game.make_move([5, 5, 5, 5])
    assert game.is_game_over()


def test_game_loop(game):
    """Test the game loop"""
    game.game()
    assert game.is_game_over() or game.state.attempts == game.state.max_attempts


def test_print_state(game):
    """Test printing the state"""
    game.print_state(debug=True)


# Tests para casos límite
def test_repeated_digits_in_guess(game):
    """Test feedback when guess contains repeated digits"""
    feedback = game.make_move([1, 1, 1, 1])
    assert feedback == Feedback(correct_position=1, correct_digit=0)

    game.state.attempts = 0  # Reset attempts for next test
    feedback = game.make_move([2, 2, 2, 2])
    assert feedback == Feedback(correct_position=0, correct_digit=1)


def test_invalid_guess_length():
    """Test handling of guesses with invalid length"""
    game = Mastermind()
    with pytest.raises(ValueError, match="Guess must be 4 digits long"):
        game.make_move([1, 2, 3])  # Too short
    with pytest.raises(ValueError, match="Guess must be 4 digits long"):
        game.make_move([1, 2, 3, 4, 5])  # Too long


def test_invalid_digit_values():
    """Test handling of guesses with invalid digit values"""
    game = Mastermind()
    with pytest.raises(ValueError, match="Digits must be between 1 and 6"):
        game.make_move([0, 1, 2, 3])  # 0 is not valid
    with pytest.raises(ValueError, match="Digits must be between 1 and 6"):
        game.make_move([1, 2, 7, 4])  # 7 is not valid
    with pytest.raises(ValueError, match="Digits must be between 1 and 6"):
        game.make_move([-1, 1, 2, 3])  # Negative numbers


def test_max_attempts_boundary():
    """Test game behavior at max attempts boundary"""
    game = Mastermind(max_attempts=1)
    assert not game.is_game_over()
    game.make_move([5, 5, 5, 5])
    assert game.is_game_over()
    with pytest.raises(ValueError, match="Game is over"):
        game.make_move([1, 2, 3, 4])


def test_multiple_games_unique_ids():
    """Test that multiple game instances have unique IDs"""
    game1 = Mastermind()
    game2 = Mastermind()
    game3 = Mastermind()
    ids = {game1.game_id, game2.game_id, game3.game_id}
    assert len(ids) == 3  # All IDs should be unique


def test_feedback_edge_cases():
    """Test edge cases for feedback calculation"""
    # All digits present but in wrong positions
    game = Mastermind()
    game.state.secret_code = [1, 2, 3, 4]
    feedback = game.make_move([4, 3, 2, 1])
    assert feedback == Feedback(correct_position=0, correct_digit=4)

    # Multiple occurrences of same digit
    game = Mastermind()
    game.state.secret_code = [1, 1, 2, 2]
    feedback = game.make_move([2, 2, 1, 1])
    assert feedback == Feedback(correct_position=0, correct_digit=4)
