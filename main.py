from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
from barcode import Code128
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
import svgutils
import datetime


currenYear = datetime.datetime.now().year
input_pdf_path = "C:\\Users\\mkoer\\Downloads\\RE-DE443MGOAEUI.pdf"
output_pdf_path = "C:\\Users\\mkoer\\Downloads\\annotated-pdf.pdf"


def getYear():
    with open('C:\\Users\\mkoer\\OneDrive\\belegnummerToPdf\\data\\integer\\currentYear.txt','r') as file:
        fileYear = " ".join(line.rstrip() for line in file)
    file.close()
    try:
        if currenYear != int(fileYear):
            updateYear(currenYear)
    except:
        updateYear(currenYear)
    fileYear = currenYear
    return fileYear


def updateYear(newYear):
    with open('C:\\Users\\mkoer\\OneDrive\\belegnummerToPdf\\data\\integer\\currentYear.txt','w') as file:
        file.write(str(newYear))
    file.close()
    resetNumbers()


def resetNumbers():
    for i in range(1, 5):
        with open(f'C:\\Users\\mkoer\\OneDrive\\belegnummerToPdf\\data\\integer\\belegnummer_{str(i)}.txt','w') as file:
            file.write("0")
        file.close()

# belegnummer_1.txt -> kontoauzugsnummer
# belegnummer_2.txt -> rechnungsnummer
# belegnummer_3.txt -> vertragsnummer
# belegnummer_4.txt -> wertpapierabrechnungsnummer

print(getYear())

packet = BytesIO()
can = canvas.Canvas(packet)
data = "RE20240000"

barcode = Code128(data)
barcode.default_writer_options['write_text'] = False
barcode.save("C:\\Users\\mkoer\\Downloads\\barcode")

svg = svgutils.transform.fromfile("C:\\Users\\mkoer\\Downloads\\barcode.svg")
originalSVG = svgutils.compose.SVG('C:\\Users\\mkoer\\Downloads\\barcode.svg')
figure = svgutils.compose.Figure(0, 0, originalSVG)
figure.save('C:\\Users\\mkoer\\Downloads\\barcode.svg')

bar = svg2rlg("C:\\Users\\mkoer\\Downloads\\barcode.svg")
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