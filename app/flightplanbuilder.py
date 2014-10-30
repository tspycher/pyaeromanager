__author__ = 'tspycher'
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, A6
from reportlab.platypus import Image, PageBreak, Spacer
from reportlab.platypus.paragraph import Paragraph
#from reportlab.lib.styles import ParagraphStyle as PS


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
        filename = os.path.join(tempfile.gettempdir(), "%s.pdf" % 'takeoff')
        elements = []
        doc = PdfTemplate(filename=filename)
        PS = doc.getStyleSheet()

        doc.loadFrames()
        elements.append(Paragraph("Takeoff Data", PS['h1']))
        elements.append(Spacer(width=1, height=5))

        elements.append(Paragraph("<b>QNH:</b> %s ft" % self.__fligthplan.performance_takeoff.qnh, PS['Normal']))
        elements.append(Paragraph("<b>OAT:</b> %s C" % self.__fligthplan.performance_takeoff.oat, PS['Normal']))
        elements.append(Paragraph("<b>PA:</b> %s ft" % self.__fligthplan.performance_takeoff.get_pa(), PS['Normal']))
        elements.append(Paragraph("<b>DA:</b> %s ft" % self.__fligthplan.performance_takeoff.get_da(), PS['Normal']))
        elements.append(Spacer(width=1, height=5))

        elements.append(Paragraph("<b>Runway No:</b> %s" % self.__fligthplan.performance_takeoff.rwy_no, PS['Normal']))
        elements.append(Paragraph("<b>Runway Ln.:</b> %s m" % self.__fligthplan.performance_takeoff.rwy_lenght, PS['Normal']))
        elements.append(Paragraph("<b>Runway Type:</b> %s" % self.__fligthplan.performance_takeoff.rwy_type, PS['Normal']))
        elements.append(Paragraph("<b>AD Code:</b> %s" % self.__fligthplan.performance_takeoff.aerodrome.code, PS['Normal']))
        elements.append(Paragraph("<b>AD Name:</b> %s" % self.__fligthplan.performance_takeoff.aerodrome.name, PS['Normal']))
        elements.append(Paragraph("<b>AD msl:</b> %s ft" % self.__fligthplan.performance_takeoff.aerodrome.msl, PS['Normal']))
        elements.append(Spacer(width=1, height=5))

        doc.build(elements)
        return filename

    def _airplane(self):
        filename = os.path.join(tempfile.gettempdir(), "%s.pdf" % 'airplane')
        airplane = self.__fligthplan.airplane

        elements = []
        doc = PdfTemplate(filename=filename)
        PS = doc.getStyleSheet()

        elements.append(Paragraph("%s %s" % (airplane.manufacturer, airplane.name), PS['Normal']))

        # Drawing Charts
        for chart in self.__fligthplan.airplane.charts:
            elements.append(PageBreak())
            elements.append(Paragraph(chart.name, PS['title']))
            elements.append(doc.image(chart.file.read()))
            elements.append(Paragraph(chart.description, PS['Normal']))


        doc.build(elements)
        return filename

    def buildPdf(self):
        to_pdffile = self._takeoff()
        ap_pdffile = self._airplane()

        output = PdfFileWriter()

        self.addAllPages(output, PdfFileReader(file(to_pdffile, "rb")))
        self.addAllPages(output, PdfFileReader(file(ap_pdffile, "rb")))

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