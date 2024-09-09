from pylate import models, indexes
from pylate.models import ColBERT
from pylate.indexes import Voyager
from typing import Tuple
import re


def sanitize_repo_name(repo_name: str) -> str:
    # If the repo_name starts with 'github:', process as a GitHub repo
    if repo_name.startswith('github:'):
        # Extract user and repo by splitting at 'github:'
        user_repo = repo_name[len('github:'):]  # remove 'github:'
        user, repo = user_repo.split('/')
        
        # Sanitize the repo part by replacing non-alphanumeric characters with '-'
        sanitized_repo = re.sub(r'[^a-zA-Z0-9]', '-', repo)
    else:
        # Sanitize the local repo by replacing non-alphanumeric characters with '-'
        sanitized_repo = re.sub(r'[^a-zA-Z0-9]', '-', repo_name)
    
    # Remove leading, trailing, and successive dashes
    sanitized_repo = re.sub(r'-+', '-', sanitized_repo)  # replace successive dashes with one
    sanitized_repo = sanitized_repo.strip('-')           # remove leading/trailing dashes
    
    if repo_name.startswith('github:'):
        return f"github-{user}-{sanitized_repo}"
    else:
        return sanitized_repo

# ColBERT model utilities

def get_model_and_index(model_name_or_path="lightonai/colbertv2.0", 
              index_folder="pylate-index", 
              index_name="index"
) -> Tuple[ColBERT, Voyager]:
    """ consistently track the RAG model for the repo """
    model = models.ColBERT(model_name_or_path)
    index = indexes.Voyager(index_folder, index_name, 
                            override=True)
    return model, index
