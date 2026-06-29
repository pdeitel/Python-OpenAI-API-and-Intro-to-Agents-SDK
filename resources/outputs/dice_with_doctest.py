from enum import Enum
import argparse
import doctest
import random


GameStatus = Enum("GameStatus", ["WON", "LOST", "CONTINUE"])


def roll_dice():
    """Roll two six-sided dice.

    Returns:
        tuple[int, int]: A pair of integers from 1 through 6.

    Examples:
        >>> dice = roll_dice()
        >>> len(dice)
        2
        >>> all(1 <= die <= 6 for die in dice)
        True
        >>> isinstance(dice, tuple)
        True
    """
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    return (die1, die2)


def display_dice(dice):
    """Display the dice roll and its total.

    Args:
        dice (tuple[int, int]): Two dice values.

    Examples:
        >>> display_dice((1, 2))
        Player rolled 1 + 2 = 3
        >>> display_dice((6, 6))
        Player rolled 6 + 6 = 12
    """
    die1, die2 = dice
    print(f"Player rolled {die1} + {die2} = {sum(dice)}")


def determine_initial_status(sum_of_dice):
    """Determine the initial game status from the first roll.

    Args:
        sum_of_dice (int): Sum of the first dice roll.

    Returns:
        tuple[GameStatus, int | None]: The game status and the point value,
        if one is established.

    Examples:
        >>> determine_initial_status(7)
        (<GameStatus.WON: 1>, None)
        >>> determine_initial_status(11)
        (<GameStatus.WON: 1>, None)
        >>> determine_initial_status(2)
        (<GameStatus.LOST: 2>, None)
        >>> determine_initial_status(3)
        (<GameStatus.LOST: 2>, None)
        >>> determine_initial_status(12)
        (<GameStatus.LOST: 2>, None)
        >>> determine_initial_status(4)
        (<GameStatus.CONTINUE: 3>, 4)
        >>> determine_initial_status(10)
        (<GameStatus.CONTINUE: 3>, 10)
    """
    match sum_of_dice:
        case 7 | 11:
            return GameStatus.WON, None
        case 2 | 3 | 12:
            return GameStatus.LOST, None
        case _:
            return GameStatus.CONTINUE, sum_of_dice


def update_game_status(sum_of_dice, my_point):
    """Update the game status after a subsequent roll.

    Args:
        sum_of_dice (int): Sum of the current dice roll.
        my_point (int): The player's established point.

    Returns:
        GameStatus: WON, LOST, or CONTINUE.

    Examples:
        >>> update_game_status(5, 5)
        <GameStatus.WON: 1>
        >>> update_game_status(7, 5)
        <GameStatus.LOST: 2>
        >>> update_game_status(8, 5)
        <GameStatus.CONTINUE: 3>
    """
    if sum_of_dice == my_point:
        return GameStatus.WON
    if sum_of_dice == 7:
        return GameStatus.LOST
    return GameStatus.CONTINUE


def play_game():
    """Play one game of craps.

    The player wins immediately on an initial roll of 7 or 11, loses
    immediately on an initial roll of 2, 3, or 12, and otherwise continues
    rolling until either the established point is rolled again or a 7 is rolled.
    """
    die_values = roll_dice()
    display_dice(die_values)

    sum_of_dice = sum(die_values)
    game_status, my_point = determine_initial_status(sum_of_dice)

    if game_status == GameStatus.CONTINUE:
        print("Point is", my_point)

    while game_status == GameStatus.CONTINUE:
        die_values = roll_dice()
        display_dice(die_values)
        sum_of_dice = sum(die_values)
        game_status = update_game_status(sum_of_dice, my_point)

    print("Player wins" if game_status == GameStatus.WON else "Player loses")


def main():
    parser = argparse.ArgumentParser(description="Play craps or run doctests.")
    parser.add_argument(
        "--doctest",
        action="store_true",
        help="run doctest unit tests with verbose output instead of playing the game",
    )
    args = parser.parse_args()

    if args.doctest:
        doctest.testmod(verbose=True)
    else:
        play_game()


if __name__ == "__main__":
    main()