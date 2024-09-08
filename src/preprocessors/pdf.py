import PyPDF2

from preprocessor import PreprocessorPlugin


class PdfPreprocessor(PreprocessorPlugin):
    """A plugin for preprocessing PDF files."""
    def can_process(self, file_path: str) -> bool:
        return file_path.lower().endswith('.pdf')

    def process(self, file_path: str) -> str:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfFileReader(file)
            text = ''
            for page in reader.pages:
                text += page.extractText()
        return text
