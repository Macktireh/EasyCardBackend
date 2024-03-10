from datetime import datetime, timedelta
from random import randint

import click
from tqdm import tqdm

from utils import printGreen


def generate() -> None:
    from repositories.cardRepository import cardRepository
    from utils.types import TypeEnum

    print()
    print("Loading data...")
    print()

    cardTypes = [
        TypeEnum.CARD_500,
        TypeEnum.CARD_1000,
        TypeEnum.CARD_2000,
        TypeEnum.CARD_5000,
        TypeEnum.CARD_10000,
    ]

    codes = []

    for _ in tqdm(range(500)):
        code = randint(100000000000, 999999999999)
        while code in codes:
            code = randint(100000000000, 999999999999)

        cardRepository.create(
            code=str(code),
            cardType=cardTypes[randint(0, len(cardTypes) - 1)],
            isValid=randint(0, 1) == 1,
            createdAt=datetime.now()
            + timedelta(days=randint(-25, -12))
            + timedelta(hours=randint(-9, 9))
            + timedelta(minutes=randint(-20, 20))
            + timedelta(seconds=randint(-20, 20)),
            updatedAt=datetime.now()
            + timedelta(days=randint(-11, -0))
            + timedelta(hours=randint(-9, 9))
            + timedelta(minutes=randint(-20, 20))
            + timedelta(seconds=randint(-20, 20)),
        )

    print()
    printGreen("Data loaded")
    print()


@click.command(name="gcards")
def gcards() -> None:
    """
    A command to load data, with no parameters and returning nothing.

    Usage:\n
        (load data): flask gcards
    """
    generate()
