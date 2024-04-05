from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
from barcode import Code128
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
import svgutils


input_pdf_path = "C:\\path\\to\\input\\file.pdf" #Path to input file
output_pdf_path = "C:\\path\\to\\output\\file.pdf" #Path to output file

packet = BytesIO()
can = canvas.Canvas(packet)
data = "RE20240000"

barcode = Code128(data)
barcode.default_writer_options['write_text'] = False
barcode.save(""C:\\path\\to\\file.pdf") #Path to svg file

svg = svgutils.transform.fromfile("C:\\path\\to\\file.pdf") #Path to svg file
originalSVG = svgutils.compose.SVG("C:\\path\\to\\file.pdf") #Path to svg file
figure = svgutils.compose.Figure(0, 0, originalSVG)
figure.save("C:\\path\\to\\file.pdf")

bar = svg2rlg("C:\\path\\to\\file.pdf") #Path to svg file
bar.scale(1.4, 0.2)

i=10
can.setFillAlpha(0.5)
can.setFillColorRGB(100, 100, 100)
can.rect(20, 32-i, 100, 28, fill=1, stroke=1)

renderPDF.draw(bar, can, 15.35, 44-i)

can.setFillAlpha(1)
can.setFillColorRGB(0, 0, 0)
pdfmetrics.registerFont(TTFont('Consolas', 'Consola.ttf'))
can.setFont("Consolas", 16.6)
can.drawString(24, 46-i, data)

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
