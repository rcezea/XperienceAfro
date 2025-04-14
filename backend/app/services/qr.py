import qrcode
# from io import BytesIO
#
# def generate_qr_code(data: str) -> BytesIO:
#     qr = qrcode.make(data)
#     img_io = BytesIO()
#     qr.save(img_io, 'PNG')
#     img_io.seek(0)
#     return img_io

from PIL import Image

def generate_qr_code(data: str) -> Image.Image:
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    return img
