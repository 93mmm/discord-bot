from PIL import Image, ImageDraw, ImageFont
from uuid import uuid4
from os import remove


class TmpImg:
    def __init__(self) -> None:
        self._fn = f"files/tmp/{uuid4()}.png"
    
    def close(self) -> None:
        remove(self._fn)
        
    def filename(self) -> str:
        return self._fn


class ImageProcessor:
    def __init__(self) -> None:
        self._font: ImageFont = ImageFont.truetype("files/fonts/m.ttf", 40)
        self._assets: dict[ImageProcessor] = dict()
    
    def __del__(self) -> None:
        for el in self._assets.values():
            el.close()
    
    def draw_assets(self, user: str) -> TmpImg:
        image: TmpImg = TmpImg()
        with Image.open("files/assets/screen.png").convert("RGBA") as img:
            d = ImageDraw.Draw(img)
            d.text((10, 10), "Hello", font=self._font, fill=(255, 255, 255, 255))
            
            with Image.open("files/assets/js.jpeg").convert("RGBA") as p:
                img.paste(im=p, box=(30, 40))
            
            fn = f"files/tmp/{uuid4()}.png"
            img.save(image.filename(), "PNG")
        return image
