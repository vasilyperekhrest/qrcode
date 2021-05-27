"""
This module contains functions that are needed to encode data (strings).
"""
import sys

import re

from source.Constants import tables, const


def digital_coding(string: str) -> str:
    """Digital coding. This type of encoding requires 10 bits per 3 characters.

    Args:
        string: String consisting of numbers.

    Returns:
        Encoded binary string.
    """
    if re.match(r"^\d+$", string) is None:
        print("Error! For digital coding, only numbers are allowed!")
        sys.exit()

    binary_string = ""

    for pos in range(0, len(string), 3):
        number = string[pos:pos+3]

        value = int(number)
        if len(number) == 3:
            binary_string += bin(value)[2::].zfill(10)
        elif len(number) == 2:
            binary_string += bin(value)[2::].zfill(7)
        else:
            binary_string += bin(value)[2::].zfill(4)

    return binary_string


def alphanumeric_coding(string: str) -> str:
    """Alphanumeric coding. This method requires 11 bits of information
    per 2 characters.

    Args:
        string: A string consisting of numbers, Latin characters and some others.

    Returns:
        Encoded binary string.
    """
    alphanum_table = tables.alphanumeric_table()

    if re.match(r'^[0-9A-Z $%*+-./:]+$', string) is None:
        print("Error! Only the following characters can be used for "
              "alphanumeric encoding:")
        print(*alphanum_table.keys())
        sys.exit()

    binary_string = ""

    for pos in range(0, len(string), 2):
        word = string[pos:pos + 2]

        if len(word) == 2:
            num_one, num_two = [alphanum_table.get(char) for char in word]
            number = num_one * 45 + num_two
            binary_string += bin(number)[2::].zfill(11)
        else:
            number = alphanum_table.get(word)
            binary_string += bin(number)[2::].zfill(6)

    return binary_string


def byte_coding(string: str) -> str:
    """Byte encoding. The data is encoded in UTF-8 encoding.

    Args:
        string: A string consisting of any characters.

    Returns:
        Encoded binary string.
    """
    byte_list = []
    for byte in bytearray(string, 'utf-8'):
        byte = bin(byte)[2::].zfill(8)
        byte_list.append(byte)

    return ''.join(byte_list)


def data_encoding(string: str, encoding_type: int) -> str:
    """A function that calls a specific encoding method.

    Args:
        string: The string to be encoded.
        encoding_type: Coding type.

    Returns:
        Encoded binary string.
    """
    if encoding_type == const.TYPE_DIGIT:
        return digital_coding(string)

    elif encoding_type == const.TYPE_BYTE:
        return byte_coding(string)

    elif encoding_type == const.TYPE_ALPHA:
        return alphanumeric_coding(string)

    else:
        raise Exception("Error! Invalid encoding type entered!")


def service_fields(
    string: str,
    encoding_type: int,
    correction_level: int,
    symbol_amount: int
) -> tuple[int, str]:
    """Determining the version, maximum block length and adding service information.

    Args:
        string: Encoded string.
        encoding_type: Coding type.
        correction_level: Correction level.
        symbol_amount: The number of characters in the original string.

    Returns:
        Version, encoded string with service information.
    """
    if correction_level == const.LEVEL_L:
        bits_table = tables.bits_table_l()

    elif correction_level == const.LEVEL_M:
        bits_table = tables.bits_table_m()

    elif correction_level == const.LEVEL_Q:
        bits_table = tables.bits_table_q()

    elif correction_level == const.LEVEL_H:
        bits_table = tables.bits_table_h()

    else:
        raise Exception("Error! Incorrect correction level entered.")

    for i, bits in enumerate(bits_table.values()):
        if bits > len(string):
            version = i + 1
            bits_amount = bits
            break
    else:
        print("Error! Too much encoded data!")
        sys.exit()

    while True:
        service_string = ""

        if 1 <= version <= 9:
            if encoding_type == const.TYPE_DIGIT:
                number = symbol_amount
                service_string += "0001" + bin(number)[2::].zfill(10)

            elif encoding_type == const.TYPE_ALPHA:
                number = symbol_amount
                service_string += "0010" + bin(number)[2::].zfill(9)

            elif encoding_type == const.TYPE_BYTE:
                number = len(string) // 8
                service_string += "0100" + bin(number)[2::].zfill(8)

        elif 10 <= version <= 26:
            if encoding_type == const.TYPE_DIGIT:
                number = symbol_amount
                service_string += "0001" + bin(number)[2::].zfill(12)

            elif encoding_type == const.TYPE_ALPHA:
                number = symbol_amount
                service_string += "0010" + bin(number)[2::].zfill(11)

            elif encoding_type == const.TYPE_BYTE:
                number = len(string) // 8
                service_string += "0100" + bin(number)[2::].zfill(16)

        elif 27 <= version <= 40:
            if encoding_type == const.TYPE_DIGIT:
                number = symbol_amount
                service_string += "0001" + bin(number)[2::].zfill(14)

            elif encoding_type == const.TYPE_ALPHA:
                number = symbol_amount
                service_string += "0010" + bin(number)[2::].zfill(13)

            elif encoding_type == const.TYPE_BYTE:
                number = len(string) // 8
                service_string += "0100" + bin(number)[2::].zfill(16)

        else:
            raise Exception("Error! Too much encoded data!")

        if len(string) + len(service_string) <= bits_amount:
            break
        else:
            version += 1
            bits_amount = bits_table.get(version)

    string = service_string + string

    delta = bits_amount - len(string)
    if delta >= 4:
        string += '0000'
    else:
        string += '0' * delta

    delta = bits_amount - len(string)
    num_byte, zero_bits = divmod(delta, 8)

    string += '0' * zero_bits

    for i in range(num_byte):
        string += '00010001' * (i % 2)
        string += '11101100' * ((i + 1) % 2)

    return version, string


def division_into_blocks(
    string: str,
    version: int,
    correction_level: int
) -> list[list[int]]:
    """Splitting the encoded string into blocks.

    Args:
        string: Encoded string with added service information.
        version: Version QR-code.
        correction_level: Correction level.

    Returns:
        List consisting of lists - blocks of information.
    """
    if correction_level == const.LEVEL_L:
        num_of_blocks = tables.blocks_table_l().get(version)

    elif correction_level == const.LEVEL_M:
        num_of_blocks = tables.blocks_table_m().get(version)

    elif correction_level == const.LEVEL_Q:
        num_of_blocks = tables.blocks_table_q().get(version)

    elif correction_level == const.LEVEL_H:
        num_of_blocks = tables.blocks_table_h().get(version)

    else:
        raise Exception("Error! Incorrect correction level entered.")

    byte_amount = len(string) // 8
    block_size, num_of_add = divmod(byte_amount, num_of_blocks)

    pos = (num_of_blocks-num_of_add) * block_size*8

    blocks = []

    for i in range(0, pos, block_size*8):
        block = []
        for k in range(i, i + block_size*8, 8):
            block.append(int(string[k:k + 8], 2))
        blocks.append(block)

    for i in range(pos, len(string), (block_size+1)*8):
        block = []
        for k in range(i, i + (block_size+1)*8, 8):
            block.append(int(string[k:k + 8], 2))
        blocks.append(block)

    return blocks


def creating_correction_bytes(
    blocks: list[list[int]],
    version: int,
    correction_level: int
) -> list[list[int]]:
    """Creation of correction blocks.

    Args:
        blocks: List consisting of lists - blocks of information.
        version: Version QR-code.
        correction_level: Correction level.

    Returns:
        List containing lists - correction blocks.
    """
    if correction_level == const.LEVEL_L:
        num_corr_byte = tables.correction_byte_table_l().get(version)

    elif correction_level == const.LEVEL_M:
        num_corr_byte = tables.correction_byte_table_m().get(version)

    elif correction_level == const.LEVEL_Q:
        num_corr_byte = tables.correction_byte_table_q().get(version)

    elif correction_level == const.LEVEL_H:
        num_corr_byte = tables.correction_byte_table_h().get(version)

    else:
        raise Exception("Error! Incorrect correction level entered.")

    gf_dict = tables.gf_table()
    gf_dict_rev = tables.gf_reversed_table()

    polynomial = tables.generating_polynomials_table().get(num_corr_byte)

    corr_blocks = []

    for block in blocks:
        array = block.copy() + [0]*abs(num_corr_byte - len(block))

        for _ in range(len(block)):
            a = array.pop(0)
            array.append(0)

            if a == 0:
                continue

            b = gf_dict_rev.get(a)
            for i, coff in enumerate(polynomial):
                c = (coff + b) % 255
                array[i] ^= gf_dict.get(c)

        corr_blocks.append(array)

    return corr_blocks


def combining_blocks(
    blocks: list[list[int]],
    correction_blocks: list[list[int]],
) -> list[int]:
    """Function for combining data blocks and correction blocks.

    Args:
        blocks: List consisting of lists - blocks of
        information.
        correction_blocks: List containing lists -
        correction blocks.

    Returns:
        A combined block that contains data from data blocks and correction blocks.
    """
    combined_block = []
    len_blocks = max([len(block) for block in blocks])
    len_corr_blocks = max([len(block) for block in correction_blocks])

    for i in range(len_blocks):
        for block in blocks:
            try:
                combined_block.append(block[i])
            except IndexError:
                pass

    for i in range(len_corr_blocks):
        for block in correction_blocks:
            try:
                combined_block.append(block[i])
            except IndexError:
                pass

    return combined_block
