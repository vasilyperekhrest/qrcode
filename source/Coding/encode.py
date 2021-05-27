import source.Coding.methods as mt


def encode(string_to_encode: str,
           encoding_type: int,
           correction_level: int
):
    string = mt.data_encoding(string_to_encode, encoding_type)
    version, string = mt.service_fields(string, encoding_type, correction_level, len(string_to_encode))
    blocks = mt.division_into_blocks(string, version, correction_level)
    corr_blocks = mt.creating_correction_bytes(blocks, version, correction_level)
    combined_block = mt.combining_blocks(blocks, corr_blocks)

    return combined_block, version
