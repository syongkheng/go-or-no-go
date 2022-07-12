import logging
import logging.config
import random

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("simpleExample")


class ScissorsPaperStone:
    r"""
    Initialise all actions that can be performed
    """
    actions = ["Scissor", "Paper", "Stone"]

    def __init__(self, uid, choice) -> None:
        r"""
        Records the unique id for statistical review
        Choice to determine who wins
        """
        self.uid = uid
        self.choice = choice
        self.program_choice = -1

    def generate_number(self) -> int:
        r"""
        Generate a number within 3 by using 6 pairs of digit
        """
        number_list = []
        while len(number_list) < 6:
            num = random.randint(1, 49)
            if num not in number_list:
                number_list.append(num)
        number_list.sort()
        self.program_choice = number_list

    def play(self) -> str:
        r"""
        Plays a game with the bot
        """
        self.generate_number()
        outcome = ScissorsPaperStone.actions[sum(self.program_choice) % 3]
        logger.debug(
            "--- Scissors Paper Stone: Program has chosen %s with numbers %s",
            outcome,
            self.program_choice,
        )
        return self.determine_result(outcome)

    def determine_result(self, outcome) -> str:
        r"""
        Determines the result of the game if it is a Win, Loss, or Draw.
        """
        if self.choice == "Stone":
            if outcome == "Scissor":
                return "Win"
            if outcome == "Paper":
                return "Lose"
        elif self.choice == "Scissor":
            if outcome == "Paper":
                return "Win"
            if outcome == "Stone":
                return "Lose"
        elif self.choice == "Paper":
            if outcome == "Stone":
                return "Win"
            if outcome == "Scissor":
                return "Lose"
        return "Draw"


def usage() -> None:
    r"""
    How to initialise, play, and get result of play
    """
    game = ScissorsPaperStone("test-uid", "Stone")
    print(game.play())


if __name__ == "__main__":
    usage()
