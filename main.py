from source import qrcode


def main() -> None:
    qr = qrcode.QRCode(4, 20, qrcode.const.TYPE_BYTE, qrcode.const.LEVEL_H)
    qr.add_data("🔥 Generator qr-code 🦄")
    qr.make(pixel_type="ellipse", bg_color="#FFDB00", pixel_color="#4312AE", with_outline=False)
    qr.show()


if __name__ == '__main__':
    main()
