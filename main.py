from source import qrcode


def main() -> None:
    qr = qrcode.QRCode(4, 8, qrcode.const.TYPE_BYTE, qrcode.const.LEVEL_H)
    qr.add_data("Hello world! 💻")
    qr.make()
    qr.show()


if __name__ == '__main__':
    main()
