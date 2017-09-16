"""Designing Flash Cards."""

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import BaseDocTemplate, PageTemplate, Paragraph, Frame, Flowable, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.lib.styles import ParagraphStyle
from math import ceil
import json

pdfmetrics.registerFont(TTFont('Garamond', 'fonts/GaramondNo8-Regular.ttf'))
pdfmetrics.registerFont(TTFont('GaramondBd', 'fonts/GaramondNo8-Bold.ttf'))
pdfmetrics.registerFont(TTFont('GaramondIt', 'fonts/GaramondNo8-Italic.ttf'))
pdfmetrics.registerFont(TTFont('GaramondBI', 'fonts/GaramondNo8-Bold-Italic.ttf'))
pdfmetrics.registerFont(TTFont('Univers', 'fonts/Univers CE 55 Medium.ttf'))
pdfmetrics.registerFont(TTFont('UniversL', 'fonts/Univers CE 45 Light.ttf'))
pdfmetrics.registerFont(TTFont('UniversLO', 'fonts/UniversCE-LightOblique.ttf'))
pdfmetrics.registerFont(TTFont('UniversBd', 'fonts/Univers CE 65 Bold.ttf'))
pdfmetrics.registerFont(TTFont('UniversIt', 'fonts/Univers CE 55 Oblique.ttf'))
pdfmetrics.registerFont(TTFont('UniversBI', 'fonts/UniversCE-BoldOblique.ttf'))
pdfmetrics.registerFont(TTFont('HelveticaC', 'fonts/Helvetica LT 57 Condensed.ttf'))
pdfmetrics.registerFont(TTFont('HelveticaCBd', 'fonts/Helvetica LT 67 Medium Condensed.ttf'))
pdfmetrics.registerFont(TTFont('HelveticaCIt', 'fonts/Helvetica LT 57 Condensed Oblique.ttf'))
pdfmetrics.registerFont(TTFont('HelveticaCBI', 'fonts/Helvetica LT 67 Medium Condensed Oblique.ttf'))
pdfmetrics.registerFont(TTFont('Arial', 'fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialBd', 'fonts/arialbd.ttf'))
pdfmetrics.registerFont(TTFont('ArialIt', 'fonts/ariali.ttf'))
pdfmetrics.registerFont(TTFont('ArialBI', 'fonts/arialbi.ttf'))

registerFontFamily('Garamond', normal='Garamond', bold='GaramondBd', italic='GaramondIt', boldItalic='GaramondBI')
registerFontFamily('Univers', normal='Univers', bold='UniversBd', italic='UniversIt', boldItalic='UniversBI')
registerFontFamily('HelveticaC', normal='HelveticaC', bold='HelveticaCBd', italic='HelveticaCIt', boldItalic='HelveticaCBI')
registerFontFamily('Arial', normal='Arial', bold='ArialBd', italic='ArialIt', boldItalic='ArialBI')
styles = getSampleStyleSheet()

styleN = ParagraphStyle('myNormal')
styleN.fontName = "Garamond"
styleN.fontsize = 11
styleN.alignment = 4
styleH = styles['Heading1']


class TextHeight():
    """Get the height of title and content of the card."""

    def __init__(self, width="", height="", title="", content=""):
        """Initialize TextHeight.

        Both title and content is added to find the height and return the
        title and content with paragraph styling
        """
        self.widthcard = width
        self.heightcard = height
        self.title = title
        self.content = content
        self.styleTitle = ParagraphStyle('myTitle')
        self.styleTitle.fontName = "Univers"
        self.styleTitle.fontSize = 10
        self.styleTitle.alignment = 1
        self.p_title = Paragraph(self.title, self.styleTitle)
        data_title = self.p_title.wrap(self.widthcard-5, 0)
        self.height_title = data_title[1]
        # print("card_title", data_title)

        self.styleContent = ParagraphStyle('myContent')
        self.styleContent.fontName = "Garamond"
        self.styleContent.fontSize = 10
        self.styleContent.alignment = 4
        self.p_content = Paragraph(self.content, self.styleContent)
        if self.content:
            data_content = self.p_content.wrap(self.widthcard-5, 0)
            self.height_content = data_content[1]
            # print("card_content", data_content)
        else:
            self.height_content = 0

    def height_return(self):
        """Return height of the title and content."""
        return self.height_title, self.height_content

    def card_return(self):
        """Return title and content with styling."""
        return self.p_title, self.p_content


class FlashCard(Flowable):
    """Flashcard with title and content."""

    def __init__(self, width="", height="", x=0, y=0, p_title="", p_content="", rect_y="", title_height="", content_height=""):
        """Initialize the flashcard using title and content."""
        Flowable.__init__(self)
        self.x = x
        self.y = y
        self.p_title = p_title
        self.p_content = p_content
        self.widthcard = width
        self.heightcard = height
        self.rect_y = rect_y
        self.content_height = content_height
        self.title_height = title_height

    def draw(self):
        """Draw the Flashcard."""
        self.p_title.wrapOn(self.canv, self.widthcard-5, self.heightcard)
        self.p_title.drawOn(self.canv, self.x+2.5, self.y-self.title_height)
        self.p_content.wrapOn(self.canv, self.widthcard-5, self.heightcard)
        self.p_content.drawOn(self.canv, self.x+2.5,  self.y - self.title_height - self.content_height - 5)
        self.canv.rect(self.x, self.rect_y, self.widthcard, self.heightcard)
        # self.canv.circle(self.x, self.y, 4, stroke=1, fill=0)


doc = BaseDocTemplate('Retreival_Practice.pdf', showBoundary=1)
print(doc.leftMargin, doc.bottomMargin, doc.width, doc.height)
f = Frame(0, 0, doc.width + doc.rightMargin + doc.leftMargin, doc.height + doc.topMargin + doc.bottomMargin, id="frame1")
PT = PageTemplate(id='firstpage', frames=[f])
PT2 = PageTemplate(id='secondpage', frames=[f])
doc.addPageTemplates([PT, PT2])
cardwidth = (doc.width + doc.rightMargin + doc.leftMargin)/4-8
cardheight = (doc.height + doc.topMargin + doc.bottomMargin)/8-16

story = []

with open('data/card.json') as data_file:
    flash_text = json.load(data_file)

flash_number = len(flash_text)
print(flash_number)
highty = 0


def rows(h, start, end):
    """Generate flashcard rows."""
    wide = 0
    for horizontal in range(start, end):
        print(horizontal, start, end)
        if horizontal >= flash_number:
            break
        try:
            data2 = flash_text[horizontal][1]
        except:
            data2 = ""
        text_height = TextHeight(width=cardwidth, height=cardheight, title=flash_text[horizontal][0], content=data2)
        title_h, content_h = text_height.height_return()
        p_title, p_content = text_height.card_return()
        flashcard = FlashCard(width=cardwidth, height=cardheight, x=wide, y=0 - h, p_title=p_title, p_content=p_content, rect_y=-cardheight - h, title_height=title_h,  content_height=content_h)
        story.append(flashcard)
        wide = wide + (doc.width + doc.rightMargin + doc.leftMargin)/4


heighty = (doc.height + doc.topMargin + doc.bottomMargin)/8

row_number = ceil(flash_number/4)
print(row_number)

count = 0
c_height = 0
for x in range(0, row_number):
    rows(c_height, count, count + 4)
    c_height = c_height + heighty
    count = count + 4
    if count % (8*4) == 0:
        c_height = 0
        story.append(PageBreak())

    print(c_height, count, count + 4)


doc.build(story)
