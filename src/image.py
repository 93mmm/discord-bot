from PIL import Image, ImageDraw, ImageFont
from uuid import uuid4
from os import remove
from random import randint

from helpers.const import UserData, Assets, Positions, Fonts
from helpers.helpers import iter_arrs

class TmpImg:
    def __init__(self) -> None:
        self._fn = f"files/tmp/{uuid4()}.png"
    
    def close(self) -> None:
        remove(self._fn)
        
    def filename(self) -> str:
        return self._fn


class ImageProcessor:
    def __init__(self) -> None:
        self._headings: ImageFont = ImageFont.truetype(Fonts.HEADINGS, 35)
        self._plain: ImageFont = ImageFont.truetype(Fonts.PLAIN, 24)
        self._assets: dict[ImageProcessor] = dict()
    
    def __del__(self) -> None:
        for el in self._assets.values():
            el.close()
    
    def _parse_text(self, text: str) -> list[str]:
        text: list[str] = text.split()
        out: list[str] = list()

        first_line: list[str] = list()
        w_index: int = 0

        for i, word in enumerate(text):
            if self._plain.getlength(" ".join(" ".join(first_line))) < Positions.FIRST_ROW_LEN:
                first_line.append(word)
                w_index = i
        text = text[w_index + 1:]
        out.append(" ".join(first_line))

        while text != list():
            next_line = list()
            for i, word in enumerate(text):
                if self._plain.getlength(" ".join(" ".join(next_line))) < Positions.NEXT_ROW_LEN:
                    next_line.append(word)
                    w_index = i
            text = text[w_index + 1:]
            out.append(" ".join(next_line))
        return out

    def draw_assets(self, user: UserData) -> TmpImg:
        image: TmpImg = TmpImg()
        with Image.open(Assets.CARD).convert("RGBA") as editable_image:
            d = ImageDraw.Draw(editable_image)
            d.text(Positions.NAME, user.name, font=self._headings, fill=(0, 0, 0, 255))
            
            for pos, txt in iter_arrs(Positions.SPECIAL_SIGNS, self._parse_text(user.special_signs)):
                d.text(pos, txt, font=self._plain, fill=(0, 0, 0, 255))
                
            for i, p in enumerate(user.get_paths()):
                with Image.open(p).convert("RGBA") as pastable:
                    editable_image.paste(im=pastable, box=Positions.PHOTO_CARDS[i], mask=pastable)

            with Image.open(Assets.PRINT).convert("RGBA") as card:
                card = card.resize(Positions.PRINT_SIZE)
                card = card.rotate(Positions.PRINT_ANGLE())
                editable_image.paste(im=card, box=Positions.PRINT_POS(), mask=card)
                
            editable_image.save(image.filename(), "PNG")
        return image
