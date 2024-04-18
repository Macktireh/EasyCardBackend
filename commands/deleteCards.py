import click

from utils import printGreen


def delete() -> None:
    from repositories.cardRepository import cardRepository

    cardRepository.deleteAll()

    print()
    printGreen("Cards deleted successfully!")
    print()


@click.command(name="dcards")
def dcards() -> None:
    """
    A command to delete data, with no parameters and returning nothing.

    Usage:\n
        (delete data): flask dcards
    """
    delete()
