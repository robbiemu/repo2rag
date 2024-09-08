import os
from typing import Generator, Tuple
from preprocessor import Preprocessor


def process_directory(
        directory_path: str, 
        without_plugins=False) -> Generator[Tuple[str, str], None, None]:
    """ use a preprocessor on files in a repository to extract text. """
    # Initialize the Preprocessor
    preprocessor = Preprocessor(without_plugins)

    # Traverse the directory
    for root, _dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                # Preprocess the file
                text = preprocessor.preprocess_file(file_path)
                # Yield the file path and extracted text of the fild
                yield file_path, text
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")