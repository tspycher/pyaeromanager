from reportlab.platypus import SimpleDocTemplate, Frame, Image, PageTemplate #, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import A6

from reportlab.lib.styles import StyleSheet1, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.units import cm, inch
from reportlab.pdfgen import canvas
from cStringIO import StringIO

class PdfTemplate(SimpleDocTemplate):
    
    fontSize1 = 6
    fontSize2 = 8
    fontSize3 = 12
    title = None

    def __init__(self, filename, title=None, **kw):
        SimpleDocTemplate.__init__(self, filename,
                                   pagesize=A6,
                                   leftMargin=11,
                                   rightMargin=11,
                                   topMargin=11,
                                   bottomMargin=11,
                                   title=title,
                                   showBoundary=0)
        self.title = title

    def loadFrames(self):
        frame1 = Frame(self.leftMargin, self.bottomMargin, self.width/2-6, self.height, id='col1')
        frame2 = Frame(self.leftMargin+self.width/2+6, self.bottomMargin, self.width/2-6, self.height, id='col2')
        self.addPageTemplates([PageTemplate(id='TwoCol',frames=[frame1,frame2]), ])

    def image(self, blobb):
        return Image(StringIO(blobb), width=200, height=160)

    def build(self, flowables):
        SimpleDocTemplate.build(self, flowables, onFirstPage=self._headerfooter, onLaterPages=self._headerfooter)

    def _headerfooter(self, canvas, doc):
        canvas.setLineWidth(1)

        canvas.saveState()
        canvas.setFont('Helvetica', 9)
        canvas.drawString(4, 410, "%s" % self.title)
        canvas.line(2, 407, 295, 407)
        canvas.setFont('Helvetica', 6)
        canvas.line(2, 10, 295, 10)
        canvas.drawString(4, 4, "PyAeromanger 14/2015 by zerodine GmbH - Thomas Spycher @tspycher")
        canvas.restoreState()

    def getStyleSheet(self):
        """Returns a stylesheet object"""
        stylesheet = StyleSheet1()

        stylesheet.add(ParagraphStyle(name='Normal',
                                      fontName='Helvetica',
                                      fontSize=self.fontSize2,
                                      leading=12,
                                      spaceBefore=4,
                                      spaceAfter=4)
                       )

        stylesheet.add(ParagraphStyle(name='DocInfo',
                                      parent=stylesheet['Normal'],
                                      leading=12,
                                      spaceBefore=0,
                                      spaceAfter=0)
                       )

        stylesheet.add(ParagraphStyle(name='Comment',
                                      fontName='Helvetica-Oblique')
                       )

        stylesheet.add(ParagraphStyle(name='Indent1',
                                      leftIndent=36,
                                      firstLineIndent=0)
                       )

        stylesheet.add(ParagraphStyle(name='BodyText',
                                      parent=stylesheet['Normal'],
                                      spaceBefore=6)
                       )
        stylesheet.add(ParagraphStyle(name='Italic',
                                      parent=stylesheet['BodyText'],
                                      fontName = 'Helvetica-Oblique')
                       )

        stylesheet.add(ParagraphStyle(name='Heading1',
                                      parent=stylesheet['Normal'],
                                      fontName = 'Helvetica-Bold',
                                      fontSize=self.fontSize3,
                                      leading=20,
                                      spaceBefore=10,
                                      spaceAfter=6),
                       alias='h1')

        stylesheet.add(ParagraphStyle(name='Heading2',
                                      parent=stylesheet['Normal'],
                                      fontName = 'Helvetica-Bold',
                                      fontSize=self.fontSize3-1,
                                      leading=18,
                                      spaceBefore=10,
                                      spaceAfter=6),
                       alias='h2')

        stylesheet.add(ParagraphStyle(name='Heading3',
                                      parent=stylesheet['Normal'],
                                      fontName = 'Helvetica-BoldOblique',
                                      fontSize=self.fontSize3-2,
                                      leading=16,
                                      spaceBefore=10,
                                      spaceAfter=6),
                       alias='h3')

        stylesheet.add(ParagraphStyle(name='Heading4',
                                      parent=stylesheet['Normal'],
                                      fontName = 'Helvetica-BoldOblique',
                                      fontsize=self.fontSize3-2,
                                      leading=14,
                                      spaceBefore=8,
                                      spaceAfter=4),
                       alias='h4')

        stylesheet.add(ParagraphStyle(name='Heading5',
                                      parent=stylesheet['Normal'],
                                      fontName = 'Helvetica-BoldOblique',
                                      fontsize=self.fontSize3-3,
                                      leading=13,
                                      spaceBefore=8,
                                      spaceAfter=4),
                       alias='h5')

        stylesheet.add(ParagraphStyle(name='Heading6',
                                      parent=stylesheet['Normal'],
                                      fontName = 'Helvetica-BoldOblique',
                                      fontSize=self.fontSize3-4,
                                      leading=12,
                                      spaceBefore=8,
                                      spaceAfter=4),
                       alias='h6')

        stylesheet.add(ParagraphStyle(name='Title',
                                      parent=stylesheet['Normal'],
                                      fontName = 'Helvetica-Bold',
                                      fontSize=self.fontSize3,
                                      leading=22,
                                      spaceAfter=8,
                                      alignment=TA_CENTER
                                      ),
                       alias='title')

        stylesheet.add(ParagraphStyle(name='Subtitle',
                                      parent=stylesheet['Normal'],
                                      fontName = 'Helvetica-Bold',
                                      fontSize=self.fontSize3,
                                      leading=self.fontSize3-2,
                                      spaceAfter=6,
                                      alignment=TA_CENTER
                                      ),
                       alias='subtitle')

        stylesheet.add(ParagraphStyle(name='TopicTitle',
                                      parent=stylesheet['Normal'],
                                      fontName = 'Helvetica-Bold',
                                      fontSize=self.fontSize3-2,
                                      leading=14,
                                      spaceAfter=6,
                                      ),
                       alias='topic-title')

        for i in range(0, 15):
            indent = 18*i
            stylesheet.add(ParagraphStyle(name='TopicItem%s' % i,
                                      parent=stylesheet['Normal'],
                                      fontName = 'Helvetica',
                                      fontSize=self.fontSize2,
                                      leftIndent=indent,
                                      spaceBefore=0,
                                      spaceAfter=0,
                                      ),
                       alias='topic-item-%s' % i)

        stylesheet.add(ParagraphStyle(name='UnorderedList',
                                      parent=stylesheet['Normal'],
                                      firstLineIndent=0,
                                      leftIndent=18,
                                      bulletIndent=9,
                                      spaceBefore=0,
                                      bulletFontName='Symbol'),
                       alias='ul')

        stylesheet.add(ParagraphStyle(name='Definition',
                                      parent=stylesheet['Normal'],
                                      firstLineIndent=0,
                                      leftIndent=36,
                                      bulletIndent=0,
                                      spaceAfter=2,
                                      spaceBefore=2,
                                      bulletFontName='Helvetica-BoldOblique'),
                       alias='dl')

        stylesheet.add(ParagraphStyle(name='OrderedList',
                                      parent=stylesheet['Definition']),
                       alias='ol')

        stylesheet.add(ParagraphStyle(name='Code',
                                      parent=stylesheet['Normal'],
                                      fontName='Courier',
                                      textColor=colors.navy,
                                      fontSize=self.fontSize1,
                                      leading=8.8,
                                      leftIndent=36,
                                      firstLineIndent=0))

        stylesheet.add(ParagraphStyle(name='FunctionHeader',
                                      parent=stylesheet['Normal'],
                                      fontName='Courier-Bold',
                                      fontSize=self.fontSize1,
                                      leading=8.8))

        stylesheet.add(ParagraphStyle(name='DocString',
                                      parent=stylesheet['Normal'],
                                      fontName='Courier',
                                      fontSize=self.fontSize1,
                                      leftIndent=18,
                                      leading=8.8))

        stylesheet.add(ParagraphStyle(name='DocStringIndent',
                                      parent=stylesheet['Normal'],
                                      fontName='Courier',
                                      fontSize=self.fontSize1,
                                      leftIndent=36,
                                      leading=8.8))

        stylesheet.add(ParagraphStyle(name='URL',
                                      parent=stylesheet['Normal'],
                                      fontName='Courier',
                                      textColor=colors.navy,
                                      alignment=TA_CENTER),
                       alias='u')

        stylesheet.add(ParagraphStyle(name='Centred',
                                      parent=stylesheet['Normal'],
                                      alignment=TA_CENTER
                                      ))

        stylesheet.add(ParagraphStyle(name='Caption',
                                      parent=stylesheet['Centred'],
                                      fontName='Helvetica-Oblique'
                                      ))

        return stylesheet