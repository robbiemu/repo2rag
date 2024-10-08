from typing import Iterator, Tuple
from pylate.models import ColBERT
from pylate.indexes import Voyager


def embed_documents(
    document_iter: Iterator[Tuple[str, str]], 
    model: ColBERT,  # ColBERT model from PyLate
    index: Voyager  # Voyager index from PyLate
) -> None:
    """
    This function takes a ColBERT model and a string of text as input, 
    and returns the embeddings generated by the model for that text.
    """
    document_dict = {file_path: text for file_path, text in document_iter}

    # Encode the documents into embeddings
    embeddings = model.encode(list(document_dict.values()), is_query=False)

    # Add the document embeddings to the index
    index.add_documents(document_ids=list(document_dict.keys()), 
                        documents_embeddings=embeddings)
