from PIL import Image, ImageDraw

from source.Point.point import Point


def rectangle(
        img: Image,
        matrix: list[list[Point]],
        border: int,
        step: int,
        pixel_color: str,
        outline_color: str
):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[j][i].bit:
                if matrix[j][i].is_pattern:
                    ImageDraw.Draw(img).rectangle(
                        ((i + border) * step,
                         (j + border) * step,
                         (i + border) * step + step,
                         (j + border) * step + step),
                        fill=pixel_color
                    )
                else:
                    ImageDraw.Draw(img).rectangle(
                        ((i + border) * step,
                         (j + border) * step,
                         (i + border) * step + step,
                         (j + border) * step + step),
                        fill=pixel_color,
                        outline=outline_color
                    )


def circle(
        img: Image,
        matrix: list[list[Point]],
        border: int,
        step: int,
        pixel_color: str,
        outline_color: str,
):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[j][i].bit:
                if matrix[j][i].is_pattern:
                    ImageDraw.Draw(img).rectangle(
                        ((i + border) * step,
                         (j + border) * step,
                         (i + border) * step + step,
                         (j + border) * step + step),
                        fill=pixel_color
                    )
                else:
                    ImageDraw.Draw(img).ellipse(
                        ((i + border) * step,
                         (j + border) * step,
                         (i + border) * step + step,
                         (j + border) * step + step),
                        fill=pixel_color,
                        outline=outline_color
                    )


def custom(
        img: Image,
        matrix: list[list[Point]],
        border: int,
        step: int,
        radius: int,
        pixel_color: str,
        outline_color: str,
):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[j][i].bit:
                if matrix[j][i].is_pattern:
                    ImageDraw.Draw(img).rectangle(
                        ((i + border) * step,
                         (j + border) * step,
                         (i + border) * step + step,
                         (j + border) * step + step),
                        fill=pixel_color
                    )
                else:
                    ImageDraw.Draw(img).rounded_rectangle(
                        ((i + border) * step,
                         (j + border) * step,
                         (i + border) * step + step,
                         (j + border) * step + step),
                        radius=radius,
                        fill=pixel_color,
                        outline=outline_color
                    )


def union(
        img: Image,
        matrix: list[list[Point]],
        border: int,
        step: int,
        radius: int,
        pixel_color: str,
        bg_color: str,
        outline_color: str,
):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if not matrix[j][i].bit:
                if not matrix[j][i].is_pattern:
                    if matrix[j][i - 1].bit and matrix[j - 1][i].bit and matrix[j - 1][i - 1].bit and i != 0 and j != 0:
                        ImageDraw.Draw(img).rectangle(
                            ((i + border) * step,
                             (j + border) * step,
                             (i + border) * step + step // 2,
                             (j + border) * step + step // 2),
                            fill=pixel_color,
                            outline=pixel_color
                        )

                    try:
                        if matrix[j][i - 1].bit and matrix[j + 1][i - 1].bit and matrix[j + 1][i].bit and i != 0:
                            ImageDraw.Draw(img).rectangle(
                                ((i + border) * step,
                                 (j + border) * step + step//2,
                                 (i + border) * step + step//2,
                                 (j + border) * step + step),
                                fill=pixel_color,
                                outline=pixel_color
                            )
                    except IndexError:
                        pass

                    try:
                        if matrix[j][i + 1].bit and matrix[j + 1][i + 1].bit and matrix[j + 1][i].bit:
                            ImageDraw.Draw(img).rectangle(
                                ((i + border) * step + step//2,
                                 (j + border) * step + step//2,
                                 (i + border) * step + step,
                                 (j + border) * step + step),
                                fill=pixel_color,
                                outline=pixel_color
                            )
                    except IndexError:
                        pass

                    try:
                        if matrix[j][i + 1].bit and matrix[j - 1][i + 1].bit and matrix[j - 1][i].bit and j != 0:
                            ImageDraw.Draw(img).rectangle(
                                ((i + border) * step + step//2,
                                 (j + border) * step,
                                 (i + border) * step + step,
                                 (j + border) * step + step//2),
                                fill=pixel_color,
                                outline=pixel_color
                            )
                    except IndexError:
                        pass

                    ImageDraw.Draw(img).rounded_rectangle(
                        ((i + border) * step + 1,
                         (j + border) * step + 1,
                         (i + border) * step + step - 1,
                         (j + border) * step + step - 1),
                        radius=radius,
                        fill=bg_color,
                        outline=bg_color
                    )

            else:
                if matrix[j][i].is_pattern:
                    ImageDraw.Draw(img).rectangle(
                        ((i + border) * step,
                         (j + border) * step,
                         (i + border) * step + step,
                         (j + border) * step + step),
                        fill=pixel_color
                    )
                else:
                    ImageDraw.Draw(img).rounded_rectangle(
                        ((i + border) * step,
                         (j + border) * step,
                         (i + border) * step + step,
                         (j + border) * step + step),
                        radius=radius,
                        fill=pixel_color,
                        outline=outline_color
                    )

                    try:
                        if matrix[j][i + 1].bit:
                            ImageDraw.Draw(img).rounded_rectangle(
                                ((i + border) * step,
                                 (j + border) * step,
                                 (i + border + 1) * step + step,
                                 (j + border) * step + step),
                                radius=radius,
                                fill=pixel_color,
                                outline=outline_color
                            )

                    except IndexError:
                        pass

                    try:
                        if matrix[j + 1][i].bit:
                            ImageDraw.Draw(img).rounded_rectangle(
                                ((i + border) * step,
                                 (j + border) * step,
                                 (i + border) * step + step,
                                 (j + border + 1) * step + step),
                                radius=radius,
                                fill=pixel_color,
                                outline=outline_color
                            )
                    except IndexError:
                        pass
