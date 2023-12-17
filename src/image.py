from PIL import ImageFont, Image, ImageDraw
from constants import PATHS, Positions
from helpers import TmpImg, User, iter_arrs, print_position, print_angle


class ImgProcessor:
    def __init__(self) -> None:
        self._headings: ImageFont = ImageFont.truetype(PATHS["headings"], 35)
        self._plain: ImageFont = ImageFont.truetype(PATHS["plain"], 24)

    def draw_assets(self, usr: User, username: str) -> TmpImg:
        image: TmpImg = TmpImg()
        with Image.open(PATHS["card"]).convert("RGBA") as canvas:
            d = ImageDraw.Draw(canvas)

            # Draw username
            d.text(Positions.USERNAME,
                   username,
                   font=self._headings,
                   fill=(0, 0, 0, 255))

            # Draw special_signs
            for pos, txt in iter_arrs(Positions.SPECIAL_SIGNS,
                                      self._parse_text(usr.special_signs)):
                d.text(pos, txt, font=self._plain, fill=(0, 0, 0, 255))

            # Draw badges
            for i, p in enumerate(usr.get_paths()):
                with Image.open(p).convert("RGBA") as badge:
                    canvas.paste(im=badge,
                                 box=Positions.BADGES[i],
                                 mask=badge)

            with Image.open(PATHS["print"]).convert("RGBA") as yoba_print:
                yoba_print = yoba_print.resize(Positions.PRINT_SIZE,
                                               Image.Resampling.LANCZOS)
                yoba_print = yoba_print.rotate(print_angle())

                canvas.paste(im=yoba_print,
                             box=print_position(),
                             mask=yoba_print)

            canvas.save(image.filename(), "PNG")
        return image

    def _parse_text(self, text: str) -> list[str]:
        def length(arr: list[str], word: str):
            text: str = " ".join(arr) + " " + word
            return self._plain.getlength(text)

        text: list[str] = text.split(" ")
        out: list[str] = list()
        row: list[str] = list()
        cut: int = 0

        for i, w in enumerate(text):
            cut = i
            if length(row, w) >= Positions.ROWS[0]:
                break
            else:
                row.append(w)
        out.append(" ".join(row))
        text = text[cut + 1:]
        row = list()

        for _ in range(2):
            for i, w in enumerate(text):
                cut = i
                if length(row, w) >= Positions.ROWS[1]:
                    break
                else:
                    row.append(w)
            text = text[cut + 1:]
            out.append(" ".join(row))
            row = list()

        print(out)
        return out
