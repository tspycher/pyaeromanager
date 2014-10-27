__author__ = 'tspycher'
from reportlab.pdfgen import canvas
from pyPdf import PdfFileReader, PdfFileWriter
import os,re

class FlightplanBuilder(object):
    __fligthplan = None

    eVfrPassword = ''
    eVfrPath = '/Users/tspycher/Dropbox/Flying/eVFRM/141016'


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
        for pdf in self.getExternalPdf(self.eVfrPath, self.__fligthplan.performance_takeoff.aerodrome.code):
            part2 = PdfFileReader(file(pdf, "rb"))
            #part2._override_encryption = True
            part2.decrypt(self.eVfrPassword)
            for pageNum in range(part2.numPages):
                output.addPage(part2.getPage(pageNum))

        # write out the merged file
        outputStream = file('output.pdf', "wb")
        output.write(outputStream)
        outputStream.close()

    def getExternalPdf(self, path, pattern):
        pdfs = []
        for (dirpath, dirnames, filenames) in os.walk(path):
            for filename in filenames:
                if re.search(pattern, filename, re.I | re.M):
                    pdfs.append(os.path.join(dirpath, filename))
        return pdfs