import sys
import os
from typing import Optional
from dotenv import load_dotenv

from embed import embed_documents
from github_downloader import GitHubDownloader
from model import get_model
from preprocess import process_directory


def retrieve(repo_name: str, branch: Optional[str], token: str, local_directory: str) -> None:
    downloader = GitHubDownloader(token, repo_name)
    downloader.download_branch(local_directory, branch=branch)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python main.py <repo_name>")
        sys.exit(1)
    
    load_dotenv()

    repo_name: str = sys.argv[1]

    local_directory: str = os.getenv("REPO2RAG_TEMP_DIR", "/tmp/repo2rag")

    token: Optional[str] = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN not found. Please set GITHUB_TOKEN in your environment or .env file.")
        sys.exit(1)

    model_name_or_path: Optional[str] = os.getenv("COLBERT_MODELNAME")
    index_folder: Optional[str] = os.getenv("COLBERT_INDEX_FOLDER")
    index_name: Optional[str] = os.getenv("COLBERT_INDEX_NAME")

    model, index = get_model(model_name_or_path, index_folder, index_name)
    
    retrieve(repo_name=repo_name, token=token, local_directory=local_directory, branch=None)
    doc_iter = process_directory(local_directory)
    embed_documents(doc_iter, model, index)
