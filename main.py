from source import qrcode


def main() -> None:
    qr = qrcode.QRCode(4, 60, qrcode.const.TYPE_BYTE, qrcode.const.LEVEL_H)
    qr.add_data("🔥 QR-code generator 🦄")
    qr.make(pixel_type="union", bg_color="#000000", pixel_color="#4312AE", radius=30)
    qr.show()


if __name__ == '__main__':
    main()
