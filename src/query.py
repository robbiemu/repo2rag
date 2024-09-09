from pylate import retrieve
from typing import Dict, List, Any
from pylate.models import ColBERT
from pylate.indexes import Voyager

from model import get_model_for_index
from preprocessor import Preprocessor

# "top-level" Library to query an index


class QueryRelay:
    """ A class to infer from a model using colBERT """
    def __init__(self, *args: Any, **kwargs: Any):
        model, index = get_model_for_index(*args, **kwargs)
        self.model: ColBERT = model
        self.index: Voyager = index

    def _query(self, queries: List[str]) -> List[List[dict]]:
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
    
    def add_text_to_result(self, result_list: List[List[Dict[str, Any]]], \
                           without_plugins: bool = False
    ) -> List[List[Dict[str, Any]]]:
        # Initialize the Preprocessor
        preprocessor = Preprocessor(without_plugins)
        
        # Process each file in result_list and add the "text" field
        for result in result_list:
            for item in result:
                file_path = item['id']
                try:
                    # Preprocess the file and add the text field
                    item['text'] = preprocessor.preprocess_file(file_path)
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")
                    item['text'] = ""  

        return result_list

    def query(self, queries: List[str]) -> List[str]:
        results = self._query(queries)
        return self._get_texts_from_ids(results)
