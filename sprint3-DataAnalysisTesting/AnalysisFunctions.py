from PyPDF2 import PdfFileReader

# local directory files, prioritise use of these in testing
# pdf path to text file (testing function)
def PDFDoctoTextDoc(source):
    """takes pdf path and saves to local directory txt file"""
    pdf = open(source, "rb")
    pdfDoc = PdfFileReader(pdf)
    text = parsePDFtoText(pdfDoc)

    # create destination path
    source = str(source) # cast to string type
    destPath = source.split(".")[0] # split off pdf extension
    
    # create text file
    with open(destPath+".txt", "w") as f:
        f.write(text)

    return destPath

# reader -> extracted text
def parsePDFtoText(pdf):
    """Takes PyPDF reader and returns its text in a string"""
    text = ""
    for page in range(0,pdf.getNumPages()):
        text += pdf.getPage(page).extract_text()
    return text
    
# local path -> reader (testing function)
def openLocalPDF(path):
    pdf = open(path, "rb")
    pdfDoc = PdfFileReader(pdf)
    return pdfDoc

