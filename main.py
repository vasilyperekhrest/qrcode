from source import qrcode


def main() -> None:
    qr = qrcode.QRCode(2, 8, qrcode.const.TYPE_BYTE, qrcode.const.LEVEL_M)
    qr.add_data("🔥 Generator qr-code 🦄")
    qr.make()
    qr.show()


if __name__ == '__main__':
    main()
