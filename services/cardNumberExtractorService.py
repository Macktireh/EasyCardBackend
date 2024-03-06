from abc import ABC, abstractmethod
from typing import List


class CardNumberExtractorService(ABC):
    @abstractmethod
    def imageToText(self, image) -> str | None:
        """
        A method to convert an image to text and return the result as a string, or None if conversion fails.

        Args:
            image (np.ndarray): The image to convert.

        Returns:
            str | None: The converted text, or None if conversion fails.
        """
        raise NotImplementedError

    @abstractmethod
    def getCardNumbers(self, image) -> List[str | None]:
        """
        A description of the entire function, its parameters, and its return types.

        Args:
            image (np.ndarray): The image to extract card numbers from.

        Returns:
            List[str | None]: A list of card numbers extracted from the image.
        """
        raise NotImplementedError
