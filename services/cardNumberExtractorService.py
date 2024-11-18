from abc import ABC, abstractmethod


class CardNumberExtractorService(ABC):
    @abstractmethod
    def getCardNumbers(self, image) -> list[str | None]:
        """
        A description of the entire function, its parameters, and its return types.

        Args:
            image (np.ndarray): The image to extract card numbers from.

        Returns:
            List[str | None]: A list of card numbers extracted from the image.
        """
        raise NotImplementedError
