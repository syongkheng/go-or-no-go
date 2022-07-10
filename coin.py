import logging
import logging.config
import random

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("simpleExample")


class Coin:
    r"""
    Initialises all coins with actions that can be performed.
    """
    faces = ["Head", "Tail"]

    def __init__(self, uid, choice) -> None:
        r"""
        Records the unique id for statistical review
        Choice to see if the flip outcome matches
        """
        self.uid = uid
        self.choice = choice
        self.program_choice = -1
        self.outcome = -1

    def generate_number(self) -> None:
        r"""
        Generate a 4 digit number between 1000 and 9999 inclusive.
        """
        self.program_choice = random.randint(1000, 9999)

    def flip(self) -> bool:
        r"""
        Flips a coin and print the outcome
        """
        self.generate_number()
        self.outcome = Coin.faces[self.program_choice % 2]
        logger.debug(
            "Coin flip: Program has chosen %s with number %s for %s",
            self.outcome,
            self.program_choice,
            self.uid,
        )
        return self.determine_outcome(self.outcome)

    def determine_outcome(self, outcome) -> bool:
        r"""
        See if the outcome matches what the user chose
        """
        if self.choice == outcome:
            return True
        return False


def usage() -> None:
    r"""
    How to initialise, flip, and get result of flip
    """
    test_coin = Coin("test_uid", "Head")
    print(test_coin.flip())


if __name__ == "__main__":
    usage()
