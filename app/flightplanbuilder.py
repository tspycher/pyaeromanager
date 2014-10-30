__author__ = 'tspycher'
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, A6
from reportlab.platypus import Image
from reportlab.platypus.paragraph import Paragraph
from reportlab.lib.styles import ParagraphStyle as PS


from pyPdf import PdfFileReader, PdfFileWriter
from .pdfcracker import PdfCracker
import npyscreen
import os,re, tempfile
from app.documents.flightplan import Flightplan
from pdftemplate import PdfTemplate

class FlightplanBuilder(object):

    """
    :type __flightplan: Flightplan
    """
    __fligthplan = None

    eVfrPassword = ''
    eVfrPath = '/Users/tspycher/Dropbox/Flying/eVFRM/141016'
    outputdir = '/Users/tspycher/Desktop'

    def __init__(self, flightplan):
        self.__fligthplan = flightplan

    def _takeoff(self):
        filename = "/tmp/takeoff.pdf"
        c = canvas.Canvas(filename, pagesize=A4)
        c.drawString(100,100,"Hello World")
        c.save()
        return filename

    def _airplane(self):
        filename = os.path.join(tempfile.gettempdir(), "%s.pdf" % 'airplane')
        airplane = self.__fligthplan.airplane

        elements = []
        doc = PdfTemplate(filename=filename, pagesize=A6)
        elements.append(Paragraph("This is text", PS('body')))

        #c = canvas.Canvas(filename, pagesize=A6)
        # General Airplane information
        #doc.drawString(10,10,"%s - %s" % (airplane.manufacturer, airplane.name))
        # Drawing Charts
        for chart in self.__fligthplan.airplane.charts:
            #doc.drawString(20, 10, chart.name)
            elements.append(doc.image(chart.file.read()))
            elements.append(Paragraph(chart.name, PS('body')))


        doc.build(elements)
        #doc.build(elements)
        return filename

    def buildPdf(self):
        to_pdffile = self._takeoff()
        ap_pdffile = self._airplane()

        output = PdfFileWriter()

        self.addAllPages(output, PdfFileReader(file(to_pdffile, "rb")))
        self.addAllPages(output, PdfFileReader(file(ap_pdffile, "rb")))

        #part11 = PdfFileReader(file(ap_pdffile, "rb"))
        #output.addPage(part11.getPage(0))

        # Add AD Info Charts
        files = dict()

        for pdf in self.getExternalPdf(self.eVfrPath, self.__fligthplan.performance_takeoff.aerodrome.code):
            files[pdf] = file(pdf, "rb")
            files["%s_" % pdf] = PdfFileReader(files[pdf])
            if files["%s_" % pdf].getIsEncrypted():
                pdfCracked = PdfCracker().crack(pdf)
                files[pdf]  = file(pdfCracked, "rb")
                files["%s_" % pdf] = PdfFileReader(files[pdf])
            self.addAllPages(output=output, input=files["%s_" % pdf])
            #for pageNum in range(files["%s_" % pdf].numPages):
            #    output.addPage(files["%s_" % pdf].getPage(pageNum))

        # write out the merged file
        outputPdf = os.path.join(self.outputdir, 'flightplan %s.pdf' % self.__fligthplan.title)
        outputStream = file(outputPdf, "wb")
        output.write(outputStream)
        outputStream.close()

        npyscreen.notify_confirm(
            message="Your pretty Fligthplan has been created at\n\n%s" % outputPdf
        )

    def addAllPages(self, output, input):
        for pageNum in range(input.numPages):
                output.addPage(input.getPage(pageNum))

    def getExternalPdf(self, path, pattern):
        pdfs = []
        for (dirpath, dirnames, filenames) in os.walk(path):
            for filename in filenames:
                if re.search(pattern, filename, re.I | re.M):
                    pdfs.append(os.path.join(dirpath, filename))
        return pdfs