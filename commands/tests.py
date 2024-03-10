from typing import Literal
from unittest import TestLoader, TextTestRunner

import click


def runTests(dir: str = "tests", pattern: str = "test*.py", verbosity: int = 2) -> Literal[0, 1]:
    tests = TestLoader().discover(start_dir=dir, pattern=pattern)
    result = TextTestRunner(verbosity=verbosity).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@click.command(name="test")
@click.option("--dir", type=click.STRING, default="tests", help="Test directory")
@click.option("--pattern", type=click.STRING, default="test*.py", help="Test pattern")
@click.option("--verbosity", type=click.INT, default=2, help="Test verbosity")
def test(dir: str, pattern: str, verbosity: int) -> None:
    """
    Run tests.

    Args:\n
        dir (str): Test directory.\n
        pattern (str): Test pattern.\n
        verbosity (int): Test verbosity.

    Usage:\n
        (run tests): flask test\n
        (run tests with directory and pattern): flask test --dir=tests/test_api --pattern=test*.py\n
        (run tests with verbose output): flask test --verbosity=2
    """
    runTests(dir, pattern, verbosity)
