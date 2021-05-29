from qrcode.Point.point import Point


def first_rule(matrix: list[list[Point]]) -> int:
    """Rule 1. Horizontally and vertically, for every 5 or more consecutive
    modules of the same color, a number of points is awarded equal to the
    length of this section minus 2.

    Args:
        matrix (list[list[Point]]): Filled QR code matrix.

    Returns:
        int: Number of points.
    """
    size = len(matrix)
    score = 0
    for i in range(size):
        if matrix[i][0].bit == 1:
            flag = True
        else:
            flag = False
        count = 1

        for j in range(1, size):
            if flag:
                if matrix[i][j].bit == 1:
                    count += 1
                else:
                    if count >= 5:
                        score += count - 2
                    flag = False
                    count = 1

            else:
                if matrix[i][j].bit == 0:
                    count += 1

                else:
                    if count >= 5:
                        score += count - 2
                    flag = True
                    count = 1

            if j == size - 1 and count >= 5:
                score += count - 2

    return score


def second_rule(matrix: list[list[Point]]) -> int:
    """Rule 2. For each 2 by 2 square of modules of the same color,
    3 points are awarded.

    Args:
        matrix (list[list[Point]]): Filled QR code matrix.

    Returns:
        int: Number of points.
    """
    score = 0
    size = len(matrix)

    for i in range(size - 1):
        for j in range(size - 1):
            a = matrix[i][j].bit
            b = matrix[i][j + 1].bit
            c = matrix[i + 1][j].bit
            d = matrix[i + 1][j + 1].bit

            if a == b == c == d:
                score += 3

    return score


def third_rule(matrix: list[list[Point]]) -> int:
    """Rule 3. For each sequence of 'BWBBBWB' modules, with 4 white modules
    on one side, 40 points are added.

    Args:
        matrix (list[list[Point]]): Filled QR code matrix.

    Returns:
        int: Number of points.
    """
    score = 0
    size = len(matrix)

    mask1 = '10111010000'
    mask2 = '00001011101'
    length = 11

    for i in range(size):
        string = ""
        # * to str
        for j in range(size):
            string += str(matrix[i][j].bit)

        pos = 0
        while pos + length <= len(string):
            substr = string[pos:pos + length]
            if substr == mask1 or substr == mask2:
                score += 40
            pos += 1

    return score


def fourth_rule(matrix: list[list[Point]]) -> int:
    """Rule 4. The number of points at this step depends on the ratio
    of the number of black and white modules.

    Args:
        matrix (list[list[Point]]): Filled QR code matrix.

    Returns:
        int: Number of points.
    """
    size = len(matrix)

    black = sum(matrix[i][j].bit for i in range(size) for j in range(size))
    black_per = abs(black/size**2 * 100 - 50)

    score = int(black_per) * 2

    return score


def make(matrix: list[list[Point]]) -> int:
    """Mask testing.

    Args:
        matrix (list[list[Point]]): Filled QR code matrix.

    Returns:
        int: Total points
    """

    # * transpose matrix
    matrix_t = []
    for j in range(len(matrix)):
        block = []
        for i in range(len(matrix)):
            block.append(matrix[i][j])
        matrix_t.append(block)

    score = 0

    score += first_rule(matrix)
    score += first_rule(matrix_t)

    score += second_rule(matrix)

    score += third_rule(matrix)
    score += third_rule(matrix_t)

    score += fourth_rule(matrix)
    return score
