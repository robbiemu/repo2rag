from pylate import retrieve
from typing import List, Any
from pylate.models import ColBERT
from pylate.indexes import Voyager

from model import get_model


class QueryRelay:
    """ A class to infer from a model using colBERT """
    def __init__(self, *args: Any, **kwargs: Any):
        model, index = get_model(*args, **kwargs)
        self.model: ColBERT = model
        self.index: Voyager = index

    def query(self, queries: List[str]) -> List[List[dict]]:
        """
        Query the model and retrieve top-k documents.

        :param queries: A list of query strings.
        :return: A list of results for each query.
        """
        # Encode query
        query_embeddings = self.model.encode(queries, is_query=True)

        # Retrieve top-k documents
        retriever = retrieve.ColBERT(index=self.index)
        results = retriever.retrieve(query_embeddings=query_embeddings, k=5)

        return results
