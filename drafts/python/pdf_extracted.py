import PyPDF2

with open('data.pdf', 'rb') as f:
    pdfReader = PyPDF2.PdfFileReader(f)

    pdfWriter = PyPDF2.PdfFileWriter()

    for i in range(33, 74):
        pdfWriter.addPage(pdfReader.getPage(i))

    with open('data_extracted.pdf', 'wb') as f:
        pdfWriter.write(f)


