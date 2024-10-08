# GitHub-to-RAG v0.1.1

This project is a UNIX tool that uses pylate (a Python library for creating and using Retrieval Augmented Generators) to create a RAG from a given GitHub repository.

## Purpose
The main purpose of this project is to provide a tool that can be used by developers and data scientists to create embeddings for a colBERT RAG based on specific GitHub repositories. This will improve the spacial efficiency in the chat context of information especially in large codebases.

## Structure
The project consists of several Python scripts:
- `main.py`: This is the main script that orchestrates the entire process. It takes a GitHub repository URL as input and creates a RAG model using pylate. 
- `src/preprocess.py`: This helper script is for preprocessing text data from GitHub repositories. It uses the Preprocessor class from src/preprocessor.py to handle different file types and extract text content accordingly. 
- `src/preprocessor.py`: This library contains a base class (Preprocessor) that handles preprocessing of text data, as well as several plugin classes for handling specific file types (PDF files, Python scripts, etc.). 
- `src/preprocessor_plugin.py`: This library contains a base class (PreprocessorPlugin) that represents a plugin for the Preprocessor class, which handles preprocessing specific types of files based on their extensions. 
- `src/preprocessors/pdf.py`: This library contains the PdfPreprocessor class, which is a plugin for the Preprocessor class and handles preprocessing of PDF files by converting them to text format using the pdf2text library.
- `src/embed.py`: This helper script is responsible for generating embeddings for the preprocessed text data using ColBERT, a state-of-the-art semantic retrieval model. 
- `src/generate.py`: This library script is responsible for generating embeddings for the text data using ColBERT model from PyLate library.
- `src/github_downloader.py`: This helper script contains functions for interacting with GitHub API to clone repositories and get information about them. 
- `src/model.py`: This library handles consistently tracking the RAG model for the repo. It uses pylate, a custom library for creating and using RAGs, which is defined in src/pylate directory. 
- `src/query.py`: This library script contains functions for querying the RAG model and generating summaries of code snippets based on user queries.

## Dependencies
This project requires Python 3.6 or later, as well as the following Python packages:
- [PyLate](https://github.com/lightonai/pylate) (a custom library for creating and using Retrieval Augmented Generators)
- [PyGithub](https://github.com/PyGithub/PyGithub)
- [PyPDF2](https://github.com/py-pdf/pypdf)
- [python-dotenv](https://github.com/theskumar/python-dotenv)

## Resources
- this project is licensed with the [LGPL3](https://choosealicense.com/licenses/gpl-3.0/) license. The [LICENSE.txt](LICENSE.txt) file contains the license locally.
- see the [TODO](TODO.md) for list of ongoing changes.
- see the [CHANGELOG](CHANGELOG.md) for a detailed history of changes
