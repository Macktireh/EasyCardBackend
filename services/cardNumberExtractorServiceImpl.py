from typing import override

from paddleocr import PaddleOCR

from config.settings import PADDLEOCR_MODEL_DIR
from services.cardNumberExtractorService import CardNumberExtractorService


class CardNumberExtractorServiceImpl(CardNumberExtractorService):
    @override
    def getCardNumbers(self, image) -> list[str | None]:
        ocr = PaddleOCR(
            use_angle_cls=True,
            lang="en",
            rec_model_dir=str(PADDLEOCR_MODEL_DIR / "rec" / "en"),
            det_model_dir=str(PADDLEOCR_MODEL_DIR / "det" / "en"),
            cls_model_dir=str(PADDLEOCR_MODEL_DIR / "cls"),
        )
        results = ocr.ocr(image, cls=True)
        listCardNumber = []
        for idx in range(len(results)):
            res = results[idx]
            for line in res:
                text: str = line[1][0].strip()
                if text and text.isdigit() and len(text) == 12:
                    listCardNumber.append(text)
                elif len(text) > 12:
                    for i in text.split(" "):
                        if len(i) == 12 and i.isdigit():
                            listCardNumber.append(i)
        return listCardNumber
