from pylate.models import ColBERT
from pylate.indexes import Voyager

from embed import embed_documents
from preprocess import process_directory

# "top-level" Library to generate embeddings

def generate_embeddings(model: ColBERT,  # ColBERT model from PyLate
                        index: Voyager,  # Voyager index from PyLate,
                        repo_path: str, # Directory with documents to be indexed
):
    # Process the directory and embed documents
    doc_iter = process_directory(repo_path)
    embed_documents(doc_iter, model, index)
