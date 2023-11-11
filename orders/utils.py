from datetime import date
from io import BytesIO
from urllib.parse import urlparse

import requests
from PIL import Image
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from orders.models import OrderCart

def generate_order_pdf(order):
    buffer = BytesIO()

    # create the PDF object
    p = canvas.Canvas(buffer, pagesize=letter)

    #---------------------------------------------
    # ORDER TEMPLATE

    p.translate(inch, inch)

    # define a large font
    p.setFont("Helvetica", 14)

    # choose some colors
    p.setStrokeColorRGB(0, 0, 0)
    p.setFillColorRGB(0, 0, 0)  # font colour
    p.drawImage('static/images/Bay-B_market_logo.png', 0,
                9.3*inch, height=0.4*inch, width=1.9*inch)
    p.drawString(0, 9 * inch, 'Warehouse No. 1234, ABCD Road')
    p.drawString(0, 8.7 * inch, 'New Delhi, ZIP:400123')
    p.setFillColorRGB(0, 0, 0)  # font colour
    p.line(0, 8.6 * inch, 6.8 * inch, 8.6 * inch)
    p.drawString(5.6 * inch, 9.5 * inch, f'Bill No: {order.order_number}')

    # get current date
    today = date.today()
    dt = today.strftime('%d-%m-%Y')
    p.drawString(5.6 * inch, 9.3 * inch, dt)

    # tax number
    p.setFont('Helvetica', 8)
    p.drawString(3*inch, 9.6*inch, 'Tax No.: #ABC1234')

    # red INVOICE on top of table
    p.setFillColorRGB(1, 0, 0)  # font colour
    p.setFont('Times-Bold', 40)
    p.drawString(4.3 * inch, 8.7 * inch, 'INVOICE')

    # # SAMPLE watermark
    # p.rotate(45)  # write at an inclined angle of 45
    # p.setFillColorCMYK(0, 0, 0, 0.8)  # font color CYAN, MAGENTA, YELLOW, BLACK
    # p.setFont('Helvetica', 140)  # font size and style
    # p.drawString(2 * inch, 1 * inch, 'SAMPLE')  # String written
    #
    # p.rotate(-45)  # restore the rotation
    # p.setFillColorRGB(0, 0, 0)  # font color

    # Table Head
    p.setFont('Times-Roman', 22)
    p.drawString(0.5 * inch, 8.3 * inch, 'Products')
    p.drawString(4 * inch, 8.3 * inch, 'Price')
    p.drawString(5 * inch, 8.3 * inch, 'Quantity')
    p.drawString(6.3 * inch, 8.3 * inch, 'Amount')

    # Table lines
    p.setStrokeColorCMYK(0, 0, 0, 1)  # vertical line color
    p.line(0.4*inch, 8.3*inch, 0.4*inch, 2.7*inch) # vertical line for
                                                    # product number
    p.line(3.9 * inch, 8.3 * inch, 3.9 * inch,
           2.7 * inch)  # first vertical line
    p.line(4.9 * inch, 8.3 * inch, 4.9 * inch,
           2.7 * inch)  # second vertical line
    p.line(6.1 * inch, 8.3 * inch, 6.1 * inch,
           2.7 * inch)  # third vertical line
    p.line(0.01 * inch, 2.5 * inch, 7 * inch,
           2.5 * inch)  # horizontal line total

    p.setFont('Times-Bold', 22)
    p.drawString(4*inch, 1.9 * inch, 'Total')
    p.setFont('Times-Roman', 22)
    p.drawString(5.6 * inch, -0.18 * inch, 'Signature')
    p.setStrokeColorRGB(0, 0, 0)  # Bottom line color
    p.line(0, -0.7 * inch, 6.8 * inch, -0.7 * inch)

    p.setFont('Helvetica', 8)  # font size
    p.setFillColorRGB(1, 0, 0)  # font color
    p.drawString(0, -0.9, u'\u00A9' + 'BayB-Marketplace')


    # # Add order details to the pdf
    products_per_user = OrderCart.objects.filter(
        user_id=order.user_id, cart_item=1)

    p.setFillColorRGB(0, 0, 0) # font color
    p.setFont('Helvetica', 14)
    row_gap = 0.6*inch # gap between each row
    line_y = 7.9*inch # location of first product line

    i = 1
    for cart_item in products_per_user:
        product = cart_item.product
        p.drawString(0.24*inch, line_y, f'{i}') # item count on order list
        p.drawString(0.6*inch, line_y, f'{product.title}')
        p.drawString(4*inch, line_y, f'{product.price}')
        p.drawString(5.5*inch, line_y, f'{cart_item.quantity}')
        p.drawString(6.5*inch, line_y, f"{cart_item.quantity * product.price}")
        line_y = line_y - row_gap
        i = i + 1

    p.setFont('Times-Bold', 22)
    p.setFillColorRGB(1, 0, 0)
    p.drawRightString(7*inch, 1.9*inch, str(order.price))

    p.setFont('Helvetica', 16)
    p.setFillColorRGB(0, 0, 0)
    p.drawString(0.6*inch, 1.5*inch, 'Recipient name: ')
    p.drawString(0.6*inch, 0.9*inch, 'Delivery address: ')
    p.setFont('Times-Bold', 16)
    p.drawString(3 * inch, 1.5 * inch, f'{order.user.first_name} '
                                       f'{order.user.last_name}')
    p.drawString(3 * inch, 0.9 * inch, f'{order.delivery_address}')

    #     # Add product image
    #     image_url = product.image.path
    #     image_ratio = int(product.image.width / product.image.height)
    #     width = int(50 * image_ratio)
    #     p.drawImage(image_url, 100, y_position - 20, width=width, height=50)
    #
    #     # adjust the vertical position for the next item
    #     y_position -= 80

    # Add grand total
    # p.drawString(100, y_position, f"Grand Total: {order.price}")

    # Save the PDF
    p.showPage()
    p.save()

    # File is ready to be written/saved
    buffer.seek(0)
    return buffer

# def generate_invoice_template(p):
#     p.translate(inch, inch)
#
#     # define a large font
#     p.setFont("Helvetica", 14)
#
#     # choose some colors
#     p.setStrokeColorRGB(0.1, 0.8, 0.1)
#     p.setFillColorRGB(0, 0, 1) # font colour
#     p.drawImage('static/images/Bay-B_market_logo.png', -0.8*inch, 9.3*inch)
#     p.drawString(0, 9*inch, 'Warehouse No. 1234, ABCD Road')
#     p.drawString(0, 8.7*inch, 'New Delhi, ZIP:400123')
#     p.setFillColorRGB(0, 0, 0) # font colour
#     p.line(0, 8.6*inch, 6.8*inch, 8.6*inch)
#     p.drawString(5.6*inch, 9.5*inch, 'Bill No: #1234')
#
#     # get current date
#     today = date.today()
#     dt = today.strftime('%d-%m-%Y')
#     p.drawString(5.6*inch, 9.3*inch, dt)
#
#     # tax number
#     p.setFont('Helvetica', 8)
#     p.drawString(3*inch, 'Tax No.: #ABC1234')
#
#     # red INVOICE on top of table
#     p.setFillColorRGB(1, 0, 0) # font colour
#     p.setFont('Times-Bold', 40)
#     p.drawString(4.3*inch, 8.7*inch, 'INVOICE')
#
#     # SAMPLE watermark
#     p.rotate(45) # write at an inclined angle of 45
#     p.setFillColorCMYK(0, 0, 0, 0.8) # font color CYAN, MAGENTA, YELLOW, BLACK
#     p.setFont('Helvetica', 140) # font size and style
#     p.drawString(2*inch, 1*inch, 'SAMPLE') # String written
#
#     p.rotate(-45) # restore the rotation
#     p.setFillColorRGB(0, 0, 0) # font color
#
#     # Table Head
#     p.setFont('Times-Roman', 22)
#     p.drawString(0.5*inch, 8.3*inch, 'Products')
#     p.drawString(4*inch, 8.3*inch, 'Price')
#     p.drawString(5*inch, 8.3*inch, 'Quantity')
#     p.drawString(6.1*inch, 8.3*inch, 'Amount')
#
#     # Table lines
#     p.setStrokeColorCMYK(0, 0, 0, 1) # vertical line color
#     p.line(3.9*inch, 8.3*inch, 3.9*inch, 2.7*inch) # first vertical line
#     p.line(4.9*inch, 8.3*inch, 4.9*inch, 2.7*inch) # second vertical line
#     p.line(6.1*inch, 8.3*inch, 6.1*inch, 2.7*inch) # third vertical line
#     p.line(0.01*inch, 2.5*inch, 7*inch, 2.5*inch) # horizontal line total
#
#     p.setFont('Times-Bold', 22)
#     p.drawString(2*inch, 0.8*inch, 'Total')
#     p.setFont('Times-Roman', 22)
#     p.drawString(5.6*inch, -0.18*inch, 'Signature')
#     p.setStrokeColorRGB(0.1, 0.8, 0.1) # Bottom line color
#     p.line(0, -0.7*inch, 6.8*inch, -0.7*inch)
#
#     p.setFont('Helvetica', 8) # font size
#     p.setFillColorRGB(1, 0, 0) # font color
#     p.drawString(0, -0.9, u'\u00A9' + 'BayB-Marketplace')
#
#     return p
