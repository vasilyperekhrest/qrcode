import sys
from PIL import Image, ImageDraw

from source.Matrix import matrix
from source.Constants import const
from source.Encoding import algorithm


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
            Encoding type:
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
        self.num_of_symbols = 0
        self.version = 0
        self.combined_block = []
        self.matrix = []
        self.size = 0
        self.img = Image.new('RGBA', (1, 1), "white")

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
            print("Error! Incorrect correction level entered.")
            sys.exit()

    def add_data(self, data: str) -> None:
        """Method for adding data to encoding.

        Args:
            data (str): The string to be encoded.
        """
        self.data = data
        self.num_of_symbols = len(data)

    def make(self) -> None:
        """Method performing QR code generation."""
        string = algorithm.data_encoding(
            self.data,
            self.encoding_type
        )

        self.version, string = algorithm.service_fields(
            string,
            self.encoding_type,
            self.correction_level,
            self.num_of_symbols
        )

        blocks = algorithm.division_into_blocks(
            string,
            self.version,
            self.correction_level
        )

        corr_blocks = algorithm.creating_correction_bytes(
            blocks,
            self.version,
            self.correction_level
        )

        algorithm.combining_blocks(
            self.combined_block,
            blocks,
            corr_blocks
        )

        self.matrix = matrix.create(
            self.combined_block,
            self.version,
            self.correction_level
        )
        self.size = len(self.matrix)

        self.img = Image.Image.resize(
            self.img,
            ((self.size + 2*self.border)*self.step,
             (self.size + 2*self.border)*self.step)
        )

        for i in range(self.size):
            for j in range(self.size):
                if self.matrix[j][i].bit == 1:
                    ImageDraw.Draw(self.img).rectangle(
                        ((i + self.border)*self.step,
                         (j + self.border)*self.step,
                         (i + self.border)*self.step + self.step,
                         (j + self.border)*self.step + self.step),
                        fill='black'
                    )

    def show(self) -> None:
        """Show qr code on screen"""
        self.img.show()

    def save(self, name="qrcode", path="", format="png") -> None:
        """Save generated QR code

        Args:
            name (str, optional): File name. Defaults to "qrcode".
            path (str, optional): File path. Defaults to "".
            format (str, optional): File extension. Defaults to "png".
        """
        self.img.save(f'{path}{name}.{format}')

    def load_img(self, name, path="", alpa=True) -> None:
        """Upload an overlay picture

        Args:
            name ([type]): File name
            path (str, optional): File path. Defaults to "".
            alpa (bool, optional): Alpha channel. Defaults to True.
        """
        img = Image.open(path+name).convert("RGBA")

        area = int(self.size**2 * self.level_coff)
        side = int(area**0.5)

        wscale = img.width / img.height
        width = round(wscale * side)
        scale = width / img.width
        height = round(scale * img.height)

        width -= 5
        height -= 5

        if width % 2 == 0:
            width -= 1
        if height % 2 == 0:
            height -= 1

        width *= self.step
        height *= self.step

        img = img.resize((width, height), Image.ANTIALIAS)

        if alpa:
            bg = img
        else:
            bg = Image.new('RGBA', img.size, 'white')
            bg.paste(img, mask=img.split()[3])

        pos_i = self.border*self.step + self.size*self.step//2 - width//2
        pos_j = self.border*self.step + self.size*self.step//2 - height//2

        self.img.paste(bg, (pos_i, pos_j), bg.split()[3])