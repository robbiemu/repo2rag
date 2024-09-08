from pylate import models, indexes
from typing import Tuple


def get_model(model_name_or_path: str, index_folder: str, 
              index_name: str) -> Tuple[models.ColBERT, indexes.Voyager]:
    """ consistently track the RAG model for the repo """
    model = models.ColBERT(model_name_or_path="lightonai/colbertv2.0")
    index = indexes.Voyager(index_folder="pylate-index", index_name="index", 
                            override=True)

    return model, index
