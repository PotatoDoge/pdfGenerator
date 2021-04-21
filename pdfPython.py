from PyPDF2 import PdfFileWriter, PdfFileReader
import io
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
import csv


import smtplib
import imghdr
from email.message import EmailMessage

# HERE GOES CORRESPONDENT'S USER AND PASS
EMAIL_ADDRESS = ''
EMAIL_PASS = ''
msg = EmailMessage()

i = 0
names = []
mails = []

# UPDATE DatosPrueba.csv file with the names and mails that you want to use
with open('pdfPython/data/DatosPrueba.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        names.append(row[0])
        mails.append(row[1])

def sendMail(msg,messages, receptor, url):
	# change the first string to your server's url and the port for an int that represents the port 		you'll be  working with
    with smtplib.SMTP_SSL('yourserevername', port) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASS)
        for message in messages:
            msg.clear()
            msg.set_content(message)
            msg['Subject'] = '' # set this string to the message that you want to send with the mail
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = receptor

            with open(url,'rb') as f:
                file_data = f.read()
                file_name = f.name

        msg.add_attachment(file_data, maintype='application',
                           subtype='octet-stream', filename=file_name)

        smtp.send_message(msg)

while  i<len(names):
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)
    # move the origin up and to the left
    c.translate(inch,inch)
    # define a large font
    c.setFont("Helvetica", 60)
    # make text go straight up
    # change color
    c.setFillColorRGB(0,0,0)
    name = names[i]
    # ADJUST THE X AND Y POSITIONS TO ONES THAT WORKS TO YOU
    xPos = 100
    yPos = 100
    c.drawString(xPos,yPos,name)
    c.save()
    # move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    # change CERTIFICADO.pdf for the original template that you want to use
	# change pdf's path
    existing_pdf = PdfFileReader(open("pdfPython/originalPDF/CERTIFICADO.pdf", "rb"))
    #print(existing_pdf.getPage(0).mediaBox)
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page2 = new_pdf.getPage(0)
    page.mergePage(page2)
    output.addPage(page)
    pddFinal = names[i]
	# change pdf's path
    pdfurl = "pdfPython/pdfs/"+pddFinal+".pdf"
    outputStream = open(pdfurl, "wb")
    output.write(outputStream)
    outputStream.close()
    #sendMail(msg,['whatever you want'], mail[i], pdfurl)
    i+=1
