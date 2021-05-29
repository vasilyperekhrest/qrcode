from source import qrcode


def main() -> None:
    qr = qrcode.QRCode(
        border=4,
        step=60,
        encoding_type=qrcode.const.TYPE_BYTE,
        correction_level=qrcode.const.LEVEL_H
    )
    qr.add_data("🔥 QR-code generator 🦄")
    qr.make(
        pixel_type="custom",
        pixel_color="#4312AE",
        bg_color="#FFDB00",
        with_outline=True,
        radius=30
    )
    qr.show()


if __name__ == '__main__':
    main()
