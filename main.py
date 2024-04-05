from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from io import BytesIO

input_pdf_path = "C:\\path\\to\\input\\file.pdf" #Path to input file
output_pdf_path = "C:\\path\\to\\output\\file.pdf" #Path to output file

packet = BytesIO()
can = canvas.Canvas(packet)

can.setFillAlpha(0.85)
can.setFillColorRGB(100, 100, 100)
can.rect(20, 20, 100, 20, fill=1, stroke=1)

can.setFillAlpha(1)
can.setFillColorRGB(255, 0, 0)
can.setFont("Helvetica", 16)
can.drawString(23, 24, "RE20240009")

can.save()

packet.seek(0)
new_pdf = PdfReader(packet)

existing_pdf = PdfReader(open(input_pdf_path, "rb"))
output = PdfWriter()

page = existing_pdf.pages[0]
page.merge_page(new_pdf.pages[0])
output.add_page(page)

with open(output_pdf_path, "wb") as outputStream:
    output.write(outputStream)
