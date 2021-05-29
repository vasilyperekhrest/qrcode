#qrcode

Module for generating qr-code.

##Usage

To create a qr-code, you need to write the following code:

```python
from source import qrcode

    
qr = qrcode.QRCode()
qr.add_data("🔥 QR-code generator 🦄")
qr.make()
qr.show()
```

##Advanced

Also, you can customize the qr-code in detail:

```python
from source import qrcode


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
```

![qrcode-image1](/Screenshots/qrcode-1.jpg)


