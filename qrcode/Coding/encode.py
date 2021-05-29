import qrcode.Coding.methods as mt


def encode(
        string_to_encode: str,
        encoding_type: int,
        correction_level: int
) -> tuple[list[int], int]:
    """A function for encoding data with a specified correction level and encoding type.

    Args:
        string_to_encode: The string to encode.
        encoding_type: Encoding type. (TYPE_BYTE, TYPE_ALPHA or TYPE_DIGIT)
        correction_level: Correction level. (LEVEL_L, LEVEL_M, LEVEL_Q or LEVEL_H)

    Returns:
        Combined block and version of qrcode.
    """
    string = mt.data_encoding(string_to_encode, encoding_type)
    version, string = mt.service_fields(string, encoding_type, correction_level, len(string_to_encode))
    blocks = mt.division_into_blocks(string, version, correction_level)
    corr_blocks = mt.creating_correction_bytes(blocks, version, correction_level)
    combined_block = mt.combining_blocks(blocks, corr_blocks)

    return combined_block, version
