from io import BytesIO
from urllib.parse import urlparse

import requests
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from orders.models import OrderCart

def generate_order_pdf(order):
    buffer = BytesIO()

    # create the PDF object
    p = canvas.Canvas(buffer, pagesize=A4)

    # Add order details to the PDF
    y_position = 750

    # Add order details to the pdf
    products_per_user = OrderCart.objects.filter(
        user_id=order.user_id, cart_item=1)

    i = 0
    for cart_item in products_per_user:
        product = cart_item.product
        p.drawString(100, y_position, f'{i}')
        p.drawString(150, y_position, f'{product.title}')
        p.drawString(300, y_position, f'{product.price}')
        p.drawString(400, y_position, f'{cart_item.quantity}')
        p.drawString(500, y_position, f"{cart_item.quantity * product.price}")
        # Add product image
        image_url = product.image.path
        image_ratio = int(product.image.width / product.image.height)
        p.drawImage(image_url, 100, y_position - 20, width=50*image_ratio, height=50)

        # adjust the vertical position for the next item
        y_position -= 80

    # Add grand total
    p.drawString(100, y_position, f"Grand Total: {order.price}")

    # Save the PDF
    p.showPage()
    p.save()

    # File is ready to be written/saved
    buffer.seek(0)
    return buffer
