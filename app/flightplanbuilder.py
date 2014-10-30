__author__ = 'tspycher'
from reportlab.pdfgen import canvas
from pyPdf import PdfFileReader, PdfFileWriter
from .pdfcracker import PdfCracker
import npyscreen
import os,re

class FlightplanBuilder(object):
    __fligthplan = None

    eVfrPassword = ''
    eVfrPath = '/Users/tspycher/Dropbox/Flying/eVFRM/141016'
    outputdir = '/Users/tspycher/Desktop'

    def __init__(self, flightplan):
        self.__fligthplan = flightplan

    def _takeoff(self):
        filename = "/tmp/takeoff.pdf"
        c = canvas.Canvas(filename)
        c.drawString(100,100,"Hello World")
        c.save()
        return filename

    def buildPdf(self):
        to_pdffile = self._takeoff()
        output = PdfFileWriter()

        part1 = PdfFileReader(file(to_pdffile, "rb"))
        output.addPage(part1.getPage(0))

        # Add AD Info Charts
        files = dict()

        for pdf in self.getExternalPdf(self.eVfrPath, self.__fligthplan.performance_takeoff.aerodrome.code):
            files[pdf] = file(pdf, "rb")
            files["%s_" % pdf] = PdfFileReader(files[pdf])
            if files["%s_" % pdf].getIsEncrypted():
                pdfCracked = PdfCracker().crack(pdf)
                files[pdf]  = file(pdfCracked, "rb")
                files["%s_" % pdf] = PdfFileReader(files[pdf])

            for pageNum in range(files["%s_" % pdf].numPages):
                output.addPage(files["%s_" % pdf].getPage(pageNum))

        # write out the merged file
        outputPdf = os.path.join(self.outputdir, 'flightplan %s.pdf' % self.__fligthplan.title)
        outputStream = file(outputPdf, "wb")
        output.write(outputStream)
        outputStream.close()

        npyscreen.notify_confirm(
            message="Your pretty Fligthplan has been created at\n\n%s" % outputPdf
        )

    def getExternalPdf(self, path, pattern):
        pdfs = []
        for (dirpath, dirnames, filenames) in os.walk(path):
            for filename in filenames:
                if re.search(pattern, filename, re.I | re.M):
                    pdfs.append(os.path.join(dirpath, filename))
        return pdfs