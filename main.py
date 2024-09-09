#!/usr/bin/env python

import sys
import os
import argparse
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), \
                           '.env') # install dir's .env
load_dotenv()

sys.path.insert(0, os.getenv('PYTHONPATH'))

from generate import generate_embeddings
from github_downloader import GitHubDownloader
from model import get_model_and_index, sanitize_repo_name


def print_defaults_help():
    """Prints default values for arguments."""
    defaults_help = """
    Default values:
    --branch: The default branch on GitHub. This is typically "main" and will be determined automatically.
    --model: Indicates the colBERT model when starting a new model, the default model name is "lightonai/colbertv2.0".
    """
    print(defaults_help)

def print_environment_help():
    """Prints environment variable requirements."""
    environment_help = """
    Environment variables:
    COLBERT_MODELNAME: The ColBERT model to use.
    GITHUB_TOKEN: GitHub access token (required for GitHub repo access).
    REPO2RAG_TEMP_DIR: Temporary directory for repo downloads (optional, defaults to "/tmp/repo2rag").
    REPO2RAG_BASE_DIR: Base directory for storing models and indices.

    These values can be set in a .env file or in your current shell environment.

    The github token must be set.
    """
    print(environment_help)

class CustomHelpAction(argparse.Action):
    def __call__(self, parser, _namespace, values, _option_string=None):
        if values == 'defaults':
            print_defaults_help()
        elif values == 'environment':
            print_environment_help()
        else:
            parser.print_help()
        sys.exit(0)


if __name__ == '__main__':
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Script to generate ColBERT \
            RAG with local or GitHub repos.", add_help=False)

    # Add custom help command for 'defaults' and 'environment'
    parser.add_argument('--help', '-h', nargs='?', action=CustomHelpAction, 
                        help="Show help message or use '--help defaults' or \
                            '--help environment' for specific help.")
    
    parser.add_argument('repo', type=str, help='Local path or "github:<repo>" \
                        for repository.')
    parser.add_argument('--branch', type=str, help='Github branch to download.')
    parser.add_argument('--model', type=str, help='ColBERT model name.', \
                        default=os.getenv("COLBERT_MODELNAME"))
    
    args = parser.parse_args()

    repo: str = args.repo
    model: str = args.model
    branch: str = args.branch

    base_directory: str = os.getenv("REPO2RAG_BASE_DIR", os.getcwd())
    temp_directory: str = os.getenv("REPO2RAG_TEMP_DIR", "/tmp/repo2rag")

    sane_name = sanitize_repo_name(repo)
    model_directory = os.path.join(base_directory, sane_name)
    index_directory = os.path.join(base_directory, sane_name)
    
    # Check if repo_name is local path or GitHub repo
    if "github:" in repo:
        token: Optional[str] = os.getenv("GITHUB_TOKEN")
        if not token:
            print("Error: GITHUB_TOKEN not found. Please set GITHUB_TOKEN in \
                  your environment or .env file.")
            sys.exit(1)

        local_directory = os.path.join(temp_directory, sane_name)
        
        downloader = GitHubDownloader(token, repo[len('github:'):])
        downloader.download_branch(local_directory, branch)
    else:
        if not os.path.isdir(repo):
            print(f"Error: '{repo}' is not a valid directory.")
            sys.exit(1)
        local_directory = repo

    # Load the model and index
    model, index = get_model_and_index(model_directory, index_directory, \
        sane_name)
    
    generate_embeddings(model, index, local_directory)
