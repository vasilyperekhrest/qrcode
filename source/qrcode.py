from PIL import Image, ImageDraw

from source.Matrix import matrix
from source.Constants import const
from source.Coding import encode


class QRCode:
    def __init__(
        self,
        border=4,
        step=8,
        encoding_type=const.TYPE_BYTE,
        correction_level=const.LEVEL_M
    ) -> None:
        """Class constructor

        Args:
            border (int, optional): The width of the white border around
            QR-code. Defaults to 4.

            step (int, optional): Single pixel size. Defaults to 8.

            encoding_type ([type], optional): Defaults to const.TYPE_BYTE.
            Coding type:
                const.TYPE_BYTE == Byte encoding

                const.TYPE_ALPHA == Alphanumeric coding

                const.TYPE_DIGIT == Digital coding

            correction_level ([type], optional): Defaults to const.LEVEL_M.
            Correction level:
                const.LEVEL_L == maximum 7% damage allowed

                const.LEVEL_M == maximum 15% damage allowed

                const.LEVEL_Q == maximum 25% damage allowed

                const.LEVEL_H == maximum 30% damage allowed
        """

        self.border = border
        self.step = step
        self.correction_level = correction_level
        self.encoding_type = encoding_type

        self.data = ""
        self.version = 0
        self.combined_block = []
        self.matrix = []
        self.size_matrix = 0
        self.img = Image.new('RGBA', (1, 1), "#6A5ACD")

        # check
        if correction_level == const.LEVEL_L:
            self.level_coff = 0.07
        elif correction_level == const.LEVEL_M:
            self.level_coff = 0.15
        elif correction_level == const.LEVEL_Q:
            self.level_coff = 0.25
        elif correction_level == const.LEVEL_H:
            self.level_coff = 0.3
        else:
            raise Exception("Error! Incorrect correction level entered.")

    def add_data(self, data: str) -> None:
        """Method for adding data to encoding.

        Args:
            data (str): The string to be encoded.
        """
        self.data = data

    def make(
            self,
            pixel_type: str = "rectangle",
            pixel_color: str = "black",
            bg_color: str = "white",
            with_outline: bool = True
    ) -> None:
        """Method performing QR code generation."""
        self.combined_block, self.version = encode.encode(
            self.data,
            self.encoding_type,
            self.correction_level
        )

        self.matrix = matrix.create(
            self.combined_block,
            self.version,
            self.correction_level
        )
        self.size_matrix = len(self.matrix)

        self.img = Image.new(
            'RGBA',
            ((self.size_matrix + 2 * self.border) * self.step,
             (self.size_matrix + 2 * self.border) * self.step),
            bg_color
        )

        if with_outline:
            outline_color = pixel_color
        else:
            outline_color = bg_color

        for i in range(self.size_matrix):
            for j in range(self.size_matrix):
                if self.matrix[j][i].bit and self.matrix[j][i].is_pattern:
                    ImageDraw.Draw(self.img).rectangle(
                        ((i + self.border) * self.step,
                         (j + self.border) * self.step,
                         (i + self.border) * self.step + self.step,
                         (j + self.border) * self.step + self.step),
                        fill=pixel_color
                    )

                elif self.matrix[j][i].bit and not self.matrix[j][i].is_pattern:
                    if pixel_type == "rectangle":
                        ImageDraw.Draw(self.img).rectangle(
                            ((i + self.border) * self.step,
                             (j + self.border) * self.step,
                             (i + self.border) * self.step + self.step,
                             (j + self.border) * self.step + self.step),
                            fill=pixel_color,
                            outline=outline_color
                        )

                    elif pixel_type == "ellipse":
                        ImageDraw.Draw(self.img).ellipse(
                            ((i + self.border) * self.step,
                             (j + self.border) * self.step,
                             (i + self.border) * self.step + self.step,
                             (j + self.border) * self.step + self.step),
                            fill=pixel_color,
                            outline=outline_color
                        )

                    else:
                        raise Exception("Error! Check pixel_type!")

    def show(self) -> None:
        """Show qr code on screen"""
        self.img.show()

    def save(self, name="qrcode", file_format="png") -> None:
        """Save generated QR code

        Args:
            name (str, optional): File name. Defaults to "qrcode".
            file_format (str, optional): File extension. Defaults to "png".
        """
        self.img.save(f'{name}.{file_format}')

    def load_img(self, name, alpha=True) -> None:
        """Upload an overlay picture

        Args:
            name ([type]): File name
            alpha (bool, optional): Alpha channel. Defaults to True.
        """
        img = Image.open(name).convert("RGBA")

        area = int(self.size_matrix ** 2 * self.level_coff)
        side = int(area**0.5)

        w_scale = img.width / img.height
        width = round(w_scale * side) - 4
        scale = width / img.width
        height = round(scale * img.height)

        if width % 2 == 0:
            width -= 1
        if height % 2 == 0:
            height -= 1

        width *= self.step
        height *= self.step

        img = img.resize((width, height), Image.ANTIALIAS)

        if alpha:
            bg = img
        else:
            bg = Image.new('RGBA', img.size_matrix, 'white')
            bg.paste(img, mask=img.split()[3])

        pos_i = self.border * self.step + self.size_matrix * self.step // 2 - width // 2
        pos_j = self.border * self.step + self.size_matrix * self.step // 2 - height // 2

        self.img.paste(bg, (pos_i, pos_j), bg.split()[3])
