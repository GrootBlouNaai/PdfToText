from flask import Flask, request
import io
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

app = Flask(__name__)

@app.route("/convert", methods=["POST"])
def convert():
    file = request.form["file"]
    filename = request.form["filename"]

    pdf = io.BytesIO(file.encode())
    resource_manager = PDFResourceManager()
    text_converter = TextConverter(resource_manager, io.StringIO())
    page_interpreter = PDFPageInterpreter(resource_manager, text_converter)
    with pdf as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)
    text = text_converter.get_results().getvalue()
    return text

if __name__ == "__main__":
    app.run(port=8000)
