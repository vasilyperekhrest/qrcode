# qrcode

Module for generating qr-code.

## Usage

To create a qr-code, you need to write the following code:

```python
from source import qrcode

    
qr = qrcode.QRCode()
qr.add_data("🔥 QR-code generator 🦄")
qr.make()
qr.show()
```

## Advanced

Also, you can customize the qr-code in detail:

```python
from source import qrcode


qr = qrcode.QRCode(
    border=4,
    step=10,
    encoding_type=qrcode.const.TYPE_BYTE,
    correction_level=qrcode.const.LEVEL_H
)
qr.add_data("🔥 QR-code generator 🦄")
qr.make(
    pixel_type="custom",
    pixel_color="#4312AE",
    bg_color="#FFDB00",
    with_outline=False,
    radius=3
)
qr.show()
```

![qrcode-image1](/Screenshots/qrcode-1.jpg)

## Presets

You can also use ready-made presets:

### Rectangle

```python
from source import qrcode


qr = qrcode.QRCode(
    border=4,
    step=10,
    encoding_type=qrcode.const.TYPE_BYTE,
    correction_level=qrcode.const.LEVEL_H
)
qr.add_data("🔥 QR-code generator 🦄")
qr.make(
    pixel_type="rectangle",
    pixel_color="#4312AE",
    bg_color="#FFDB00",
    with_outline=True,
)
qr.show()
```

![qrcode-image2](/Screenshots/qrcode-2.jpg)

### Circle

```python
from source import qrcode


qr = qrcode.QRCode(
    border=4,
    step=10,
    encoding_type=qrcode.const.TYPE_BYTE,
    correction_level=qrcode.const.LEVEL_H
)
qr.add_data("🔥 QR-code generator 🦄")
qr.make(
    pixel_type="circle",
    pixel_color="#4312AE",
    bg_color="#FFDB00",
    with_outline=True,
)
qr.show()
```

![qrcode-image3](/Screenshots/qrcode-3.jpg)

### Union

```python
from source import qrcode


qr = qrcode.QRCode(
    border=4,
    step=10,
    encoding_type=qrcode.const.TYPE_BYTE,
    correction_level=qrcode.const.LEVEL_H
)
qr.add_data("🔥 QR-code generator 🦄")
qr.make(
    pixel_type="union",
    pixel_color="#4312AE",
    bg_color="#FFDB00"
)
qr.show()
```

![qrcode-image4](/Screenshots/qrcode-4.jpg)
