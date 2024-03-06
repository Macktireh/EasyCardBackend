from getpass import getpass

import click

from repositories.userRepository import userRepository
from utils import printGreen, printRed
from validators.authValidator import AuthValidator


def createSuperUserCli() -> None:
    while True:
        email = input("Enter email address [admin@example.com]: ") or "admin@example.com"
        if email == "":
            printRed("Email is required.")
            continue
        if not AuthValidator.validateEmail(email):
            printRed("Email is invalid.")
            continue
        if userRepository.exists(email=email):
            printRed("A user with this e-mail address already exists.")
            continue

        name = input("Enter name [John Doe]: ") or "John Doe"

        while True:
            password = getpass("Enter password: ")
            if password == "":
                printRed("Password is required.")
                continue

            confirmPassword = getpass("Enter password again: ")
            if confirmPassword != password:
                printRed("Password and Confirm Password doesn't match.")
                continue

            break

        data = {
            "email": email,
            "name": name,
            "password": password,
        }

        userRepository.createSuperUser(**data)

        printGreen("\nSuper user successfully created.\n")

        break


@click.command(name="createsuperuser")
def createsuperuser() -> None:
    """
    Create a super user.

    Usage:\n
        (create super user): flask createsuperuser
    """
    createSuperUserCli()
