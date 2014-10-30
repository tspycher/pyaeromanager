from reportlab.platypus import SimpleDocTemplate, Image #, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import A6
from cStringIO import StringIO

class PdfTemplate(SimpleDocTemplate):
    def image(self, blobb):
        return Image(StringIO(blobb), width=200, height=160)

