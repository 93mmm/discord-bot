from PIL import Image, ImageDraw, ImageFont
from uuid import uuid4
from os import remove
from src.helpers.const import UserData, Assets, Positions, Fonts
from src.helpers.helpers import iter_arrs


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
        increment: int = 0

        while self._plain.getlength(" ".join(text[:increment])) < Positions.FIRST_ROW_LEN and increment < len(text):
            increment += 1
        else:
            out.append(" ".join(text[:increment - 1]))
            text = text[increment - 1:]

        while text != list():
            while self._plain.getlength(" ".join(text[:increment])) < Positions.NEXT_ROW_LEN and increment < len(text):
                increment += 1
            else:
                out.append(" ".join(text[:increment - 1]))
                text = text[increment - 1:]

        return out
    
    def draw_assets(self, user: UserData) -> TmpImg:
        image: TmpImg = TmpImg()
        with Image.open(Assets.CARD).convert("RGBA") as editable_image:
            d = ImageDraw.Draw(editable_image)
            d.text(Positions.NAME, user.name, font=self._headings, fill=(0, 0, 0, 255))
            
            for pos, txt in iter_arrs(Positions.SPECIAL_SIGNS, self._parse_text(user.special_signs)):
                d.text(pos, txt, font=self._plain, fill=(0, 0, 0, 255))
                
            for i, p in enumerate(user.photo_paths):
                with Image.open(p).convert("RGBA") as pastable:
                    editable_image.paste(im=pastable, box=Positions.PHOTO_CARDS[i], mask=pastable)

            editable_image.save(image.filename(), "PNG")
            editable_image.show()
        return image
