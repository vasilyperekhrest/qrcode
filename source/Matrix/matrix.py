from itertools import product
from typing import Callable

from source.Point.point import Point
from source.Constants import tables, const
from source.Matrix import tests


def search_patterns(matrix: list[list[Point]], x: int, y: int) -> None:
    """Adding search patterns.

    Args:
        matrix: Matrix containing qr code pixels.
        x: X coordinate.
        y: Y coordinate.
    """
    for i in range(7):
        matrix[x + i][y].bit = True
        matrix[x + i][y].is_service_bit = True
        matrix[x + i][y].is_pattern = True

        matrix[x][y + i].bit = True
        matrix[x][y + i].is_service_bit = True
        matrix[x][y + i].is_pattern = True

        matrix[x+6][y+i].bit = True
        matrix[x+6][y+i].is_service_bit = True
        matrix[x+6][y+i].is_pattern = True

        matrix[x+i][y+6].bit = True
        matrix[x+i][y+6].is_service_bit = True
        matrix[x+i][y+6].is_pattern = True

    for i in range(3):
        matrix[x+2+i][y+2].bit = True
        matrix[x+2+i][y+2].is_service_bit = True
        matrix[x+2+i][y+2].is_pattern = True

        matrix[x+2][y+2+i].bit = True
        matrix[x+2][y+2+i].is_service_bit = True
        matrix[x+2][y+2+i].is_pattern = True

        matrix[x+4][2+y+i].bit = True
        matrix[x+4][y+2+i].is_service_bit = True
        matrix[x+4][y+2+i].is_pattern = True

        matrix[x+2+i][y+4].bit = True
        matrix[x+2+i][y+4].is_service_bit = True
        matrix[x+2+i][y+4].is_pattern = True

    matrix[x+3][y+3].bit = True
    matrix[x+3][y+3].is_service_bit = True
    matrix[x+3][y+3].is_pattern = True

    for i in range(9):
        for j in range(9):
            index_i = x + i - 1
            index_j = y + j - 1

            if 0 <= index_i < len(matrix) and 0 <= index_j < len(matrix):
                if not matrix[x+i-1][y+j-1].is_service_bit:
                    matrix[x+i-1][y+j-1].is_service_bit = True
                    matrix[x+i-1][y+j-1].is_pattern = True


def sync_strips(matrix: list[list[Point]]) -> None:
    """Adding sync bars.

    Args:
        matrix: Matrix containing qr code pixels.
    """
    count = (len(matrix) - 14) // 2

    for i in range(1, count+1):
        matrix[i * 2 + 6][6].bit = True
        matrix[i * 2 + 6][6].is_service_bit = True
        matrix[i * 2 + 5][6].is_service_bit = True
        matrix[i * 2 + 7][6].is_service_bit = True

        matrix[6][i * 2 + 6].bit = True
        matrix[6][i * 2 + 6].is_service_bit = True
        matrix[6][i * 2 + 5].is_service_bit = True
        matrix[6][i * 2 + 7].is_service_bit = True


def mask_correction_level(matrix: list[list[Point]], mask: str) -> None:
    """Adding mask code and correction level.

    Args:
        matrix: Matrix containing qr code pixels.
        mask: Mask code.
    """
    index = 0
    pos_bit = 0
    while index <= 8:
        if index == 6:
            index += 1

        matrix[8][index].is_service_bit = True
        matrix[8][index].bit = int(mask[pos_bit])
        pos_bit += 1
        index += 1

    index = 7
    while index >= 0:
        if index == 6:
            index -= 1
        matrix[index][8].is_service_bit = True
        matrix[index][8].bit = int(mask[pos_bit])
        pos_bit += 1
        index -= 1

    pos_bit = 0
    index = len(matrix)-1
    while index >= len(matrix)-7:
        matrix[index][8].is_service_bit = True
        matrix[index][8].bit = int(mask[pos_bit])
        pos_bit += 1
        index -= 1

    index = len(matrix)-8
    while index <= len(matrix)-1:
        matrix[8][index].is_service_bit = True
        matrix[8][index].bit = int(mask[pos_bit])
        pos_bit += 1
        index += 1


def alignment_patterns(matrix: list[list[Point]], version: int) -> None:
    """Adding alignment patterns (from version 2).

    Args:
        matrix: Matrix containing qr code pixels.
        version: QR code version.
    """
    if version > 1:
        patterns = tables.alignment_patterns_table().get(version)

        if version > 6:
            points = list(product(patterns, patterns))
            points.remove((patterns[0], patterns[0]))
            points.remove((patterns[0], patterns[-1]))
            points.remove((patterns[-1], patterns[0]))
        else:
            points = [(patterns[0], patterns[0])]

        for x, y in points:
            matrix[x][y].bit = True
            matrix[x][y].is_service_bit = True

            for i in range(5):
                matrix[x - 2][y - 2 + i].bit = True
                matrix[x - 2][y - 2 + i].is_service_bit = True

                matrix[x + 2][y - 2 + i].bit = True
                matrix[x + 2][y - 2 + i].is_service_bit = True

                matrix[x - 2 + i][y - 2].bit = True
                matrix[x - 2 + i][y - 2].is_service_bit = True

                matrix[x - 2 + i][y + 2].bit = True
                matrix[x - 2 + i][y + 2].is_service_bit = True

            for i in range(5):
                for j in range(5):
                    if not matrix[x - 2 + i][y - 2 + j].is_service_bit:
                        matrix[x - 2 + i][y - 2 + j].is_service_bit = True


def version_code(matrix: list[list[Point]], version: int) -> None:
    """Adding version code (from version 7).

    Args:
        matrix: Matrix containing qr code pixels.
        version: QR code version.
    """
    if version > 6:
        codes = tables.version_code_table().get(version)

        pos = len(matrix) - 11

        for i in range(6):
            # left down
            matrix[pos][i].bit = int(codes[0][i])
            matrix[pos][i].is_service_bit = True

            matrix[pos + 1][i].bit = int(codes[1][i])
            matrix[pos + 1][i].is_service_bit = True

            matrix[pos + 2][i].bit = int(codes[2][i])
            matrix[pos + 2][i].is_service_bit = True

            # right up
            matrix[i][pos].bit = int(codes[0][i])
            matrix[i][pos].is_service_bit = True

            matrix[i][pos + 1].bit = int(codes[1][i])
            matrix[i][pos + 1].is_service_bit = True

            matrix[i][pos + 2].bit = int(codes[2][i])
            matrix[i][pos + 2].is_service_bit = True


def fill_data(
    matrix: list[list[Point]],
    comb_blocks: list[int],
    mask: Callable[[int, int], int]
) -> None:
    """Adding data to qr code matrix.

    Args:
        matrix: Matrix containing qr code pixels.
        comb_blocks: Data blocks.
        mask: Lambda function of a specific mask.
    """
    size = len(matrix)

    pos_i = size - 1
    pos_j = pos_i

    # down=False or up=True
    flag = True

    flag_step = False

    for byte in comb_blocks:
        byte = bin(byte)[2::].zfill(8)
        if pos_j == -1:
            break

        for char in byte:
            if pos_j == -1:
                break

            ready = False
            while not ready:
                if pos_j == -1:
                    break

                if pos_j == 6:
                    pos_j -= 1

                if flag:
                    if not matrix[pos_i][pos_j].is_service_bit:
                        matrix[pos_i][pos_j].bit = int(char)

                        if mask(pos_i, pos_j) == 0:
                            matrix[pos_i][pos_j].bit ^= 1

                        ready = True

                    if not flag_step:
                        pos_j -= 1
                        flag_step = True
                    else:
                        pos_j += 1
                        pos_i -= 1
                        flag_step = False

                    if pos_i == -1:
                        pos_i += 1
                        pos_j -= 2
                        flag = False

                else:
                    if not matrix[pos_i][pos_j].is_service_bit:
                        matrix[pos_i][pos_j].bit = int(char)

                        if mask(pos_i, pos_j) == 0:
                            matrix[pos_i][pos_j].bit ^= 1

                        ready = True

                    if not flag_step:
                        pos_j -= 1
                        flag_step = True
                    else:
                        pos_j += 1
                        pos_i += 1
                        flag_step = False

                    if pos_i == len(matrix):
                        pos_i -= 1
                        pos_j -= 2
                        flag = True


def create(
    comb_blocks: list[int],
    version: int,
    correction_level: int
) -> list[list[Point]]:
    """Generating a QR Code Matrix.

    Args:
        comb_blocks: Data blocks.
        version: QR code version.
        correction_level: Correction level

    Returns:
        QR Code Matrix.
    """
    size = tables.qrcode_size_table().get(version)
    matrix = [[Point() for _ in range(size)] for _ in range(size)]
    scores = {}

    if correction_level == const.LEVEL_L:
        codes_mask_table = tables.mask_table_l()

    elif correction_level == const.LEVEL_M:
        codes_mask_table = tables.mask_table_m()

    elif correction_level == const.LEVEL_Q:
        codes_mask_table = tables.mask_table_q()

    elif correction_level == const.LEVEL_H:
        codes_mask_table = tables.mask_table_h()

    else:
        raise Exception("Error! Incorrect correction level entered.")

    func_mask_table = tables.mask_table()

    search_patterns(matrix, 0, 0)
    search_patterns(matrix, size-7, 0)
    search_patterns(matrix, 0, size-7)

    matrix[size - 8][8].bit = True
    matrix[size-8][8].is_service_bit = True

    alignment_patterns(matrix, version)
    version_code(matrix, version)
    sync_strips(matrix)

    for num in range(8):
        mask_code = codes_mask_table.get(num)
        mask_correction_level(matrix, mask_code)

        func_mask = func_mask_table.get(num)
        fill_data(matrix, comb_blocks, func_mask)

        score = tests.make(matrix)
        scores[score] = num

    min_score = min(scores.keys())
    num_mask = scores.get(min_score)

    mask_code = codes_mask_table.get(num_mask)
    mask_correction_level(matrix, mask_code)

    func_mask = func_mask_table.get(num_mask)
    fill_data(matrix, comb_blocks, func_mask)

    return matrix
