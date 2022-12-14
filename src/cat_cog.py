from io import BytesIO
import logging

from PIL import Image, ImageDraw, ImageFont, ImageSequence
from PIL.Image import Image as ImageType
from PIL.ImageDraw import ImageDraw as DrawerType
from httpx import get
from discord import (
    ApplicationContext,
    Bot,
    Cog,
    File,
    slash_command,
)

logger = logging.getLogger(__name__)

JPG_URL = "https://api.thecatapi.com/v1/images/search?mime_types=jpg,png&format=src"
GIF_URL = "https://api.thecatapi.com/v1/images/search?mime_types=gif&format=src"

FONT_FILE_LOCATION = "../impact.ttf"

MAX_RETRY_ATTEMPTS = 10


class BaseImage:
    def __init__(self, text: str) -> None:
        self._text = self._prepare_text(text)
        self._texted_img: ImageType | list[ImageType]

    def create_stream(self) -> BytesIO:
        raise NotImplementedError

    def _add_text(self, orig_img: bytes, text: str) -> list[ImageType] | ImageType:
        raise NotImplementedError

    def _load_image(self, url: str) -> bytes:
        orig_img = get(url, follow_redirects=True, timeout=20)
        return orig_img.content

    def _prepare_text(self, text: str) -> str:
        correctly_spaced_chars = []

        img_formats = [".jpg", ".gif"]
        if text[-4:] in img_formats:
            text = text[:-4]

        for char in text:
            if char == "_":
                correctly_spaced_chars.append("\n")
            elif char == "-":
                correctly_spaced_chars.append(" ")
            else:
                correctly_spaced_chars.append(char)
        return "".join([c for c in correctly_spaced_chars]).upper()


class StaticImage(BaseImage):
    _URL = JPG_URL

    def __init__(self, text: str) -> None:
        super().__init__(text)
        self._orig_img = self._load_image(self._URL)
        self._texted_img: ImageType = self._add_text(self._orig_img, self._text)

    def _add_text(self, orig_img: bytes, text: str) -> ImageType:
        img = Image.open(BytesIO(orig_img))
        drawer: DrawerType = ImageDraw.Draw(img)
        font = ImageFont.truetype(FONT_FILE_LOCATION, int(img.height * 0.1))

        drawer.text(
            xy=(img.width // 2, img.height - 20),
            text=text,
            font=font,
            fill=(255, 255, 255),
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            anchor="md",
            align="center",
        )

        return img

    def create_stream(self) -> BytesIO:
        stream: BytesIO = BytesIO()
        source = self._texted_img

        source.save(stream, format="jpeg", optimize=True)

        stream.seek(0)
        return stream


class GIF(BaseImage):
    _URL = GIF_URL
    _MAX_RETRY_ATTEMPTS = MAX_RETRY_ATTEMPTS

    def __init__(self, text: str) -> None:
        super().__init__(text)

        fail_count = 0
        while True:
            if fail_count >= self._MAX_RETRY_ATTEMPTS:
                raise Exception("Too many retry attempts")

            try:
                self._orig_img = self._load_image(self._URL)
                self._texted_img: list[ImageType] = self._add_text(self._orig_img, self._text)
            except ValueError as e:
                if e.args[0] == "cannot allocate more than 256 colors":
                    fail_count += 1
                    continue
                raise
            break

    def _add_text(self, orig_img: bytes, text: str) -> list[ImageType]:
        img = Image.open(BytesIO(orig_img))
        font = ImageFont.truetype(FONT_FILE_LOCATION, int(img.height * 0.1))
        frames: list[ImageType] = []

        for frame in ImageSequence.Iterator(img):
            drawer: DrawerType = ImageDraw.Draw(frame)
            drawer.text(
                xy=(img.width // 2, img.height - 20),
                text=text,
                font=font,
                fill=(255, 255, 255),
                stroke_width=2,
                stroke_fill=(0, 0, 0),
                anchor="md",
                align="center",
            )
            # except "ValueError('cannot allocate more than 256 colors')"
            # fill=0, stroke_fill=255 or some other num
            # see https://getridbug.com/python/valueerror-cannot-allocate-more-than-256-colors-when-using-imagedraw-draw/ # noqa: E501
            # for now just retry
            del drawer

            stream = BytesIO()
            frame.save(stream, format="GIF")
            frame = Image.open(stream)

            frames.append(frame)

        return frames

    def create_stream(self) -> BytesIO:
        stream = BytesIO()
        source = self._texted_img

        source[0].save(stream, save_all=True, format="GIF", append_images=source[1:])

        stream.seek(0)
        return stream


class Cat(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command()  # type: ignore
    async def cat(self, ctx: ApplicationContext, text: str) -> None:
        """Sends cat pic."""
        await ctx.respond(file=File(fp=StaticImage(text).create_stream(), filename="cat.jpg"))

    @slash_command()  # type: ignore
    async def gif(self, ctx: ApplicationContext, text: str) -> None:
        """Sends cat gif."""
        await ctx.respond(file=File(fp=GIF(text).create_stream(), filename="cat.gif"))


def setup(bot: Bot) -> None:
    bot.add_cog(Cat(bot))
