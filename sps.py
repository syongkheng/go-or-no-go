import logging
import logging.config
import random


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
        self.win = None

    def play(self) -> str:
        r"""
        Plays a game with the bot
        """
        logger.info("Scissors Paper Stone in progress with %s", self.uid)
        program_choice = random.randint(0, 999)
        outcome = ScissorsPaperStone.actions[program_choice % 3]
        logger.debug("Program has chosen %s with number %s", outcome, program_choice)
        return self.determine_result(outcome)

    def determine_result(self, outcome) -> str:
        r"""
        Determines the result of the game if it is a Win, Loss, or Draw.
        """
        logger.debug(
            "Within determining result of choice: %s and outcome: %s",
            self.choice,
            outcome,
        )
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
    logging.config.fileConfig("logging.conf")
    logger = logging.getLogger("simpleExample")
