import os
from typing import List, override

import cv2
import pytesseract

from config.settings import PATH_TESSERACT_CMD
from services.cardNumberExtractorService import CardNumberExtractorService

if os.name == "nt":
    if not PATH_TESSERACT_CMD:
        raise Exception("Add path environment variable TESSERACT_CMD")
    pytesseract.pytesseract.tesseract_cmd = PATH_TESSERACT_CMD


class CardNumberExtractorServiceImpl(CardNumberExtractorService):
    @override
    def imageToText(self, image) -> str | None:
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            _, threshed = cv2.threshold(gray, 127, 255, cv2.THRESH_TRUNC)
            return pytesseract.image_to_string(threshed, lang="eng", config="--psm 6")
        except Exception as e:
            print(str(e) + " Add path environment variable TESSERACT_CMD")
            return None

    @override
    def getCardNumbers(self, image) -> List[str | None]:
        listCardNumber = []
        texts = self.imageToText(image).split()
        for text in texts:
            if len(text) == 12 and text.isdigit():
                listCardNumber.append(text)
            elif len(text) > 12:
                for i in text.split(" "):
                    if len(i) == 12 and i.isdigit():
                        listCardNumber.append(i)
        return listCardNumber
