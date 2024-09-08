from github import Github, Repository, ContentFile
import os
from typing import List, Optional

class GitHubDownloader:
    def __init__(self, token: str, repo_name: str):
        """
        Initialize the downloader with the GitHub token and repository name.
        :param token: Personal access token for GitHub.
        :param repo_name: Repository in the format 'owner/repo'.
        """
        self.github = Github(token)
        self.repo: Repository.Repository = self.github.get_repo(repo_name)
    
    def get_main_branch(self) -> str:
        """
        Retrieve the default branch of the repository.
        :return: The default branch name.
        """
        return self.repo.default_branch

    def _download_file(self, file_content: ContentFile.ContentFile, 
                       save_dir: str) -> None:
        """
        Helper function to download a single file from the repository.
        :param file_content: The file content object from the GitHub API.
        :param save_dir: The directory to save the file in.
        """
        file_path = os.path.join(save_dir, file_content.path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'wb') as file:
            file.write(file_content.decoded_content)
        print(f"Downloaded: {file_content.path}")
    
    def _download_directory(self, contents: List[ContentFile.ContentFile], 
                            save_dir: str, branch: str) -> None:
        """
        Recursively download the contents of a directory.
        :param contents: List of file and directory contents.
        :param save_dir: The directory to save files.
        :param branch: The branch from which to download files.
        """
        for content in contents:
            if content.type == 'dir':
                # Recursively download subdirectories
                subdir_contents = self.repo\
                    .get_contents(content.path, ref=branch)
                self._download_directory(subdir_contents, save_dir, branch)
            else:
                # Download the file
                self._download_file(content, save_dir)

    def download_branch(self, save_dir: str, 
                        branch: Optional[str] = None) -> None:
        """
        Download the contents of a branch to a local directory.
        :param save_dir: The local directory to save the files.
        :param branch: The branch to download from (default is the main branch).
        """
        # Fallback to default branch if none is provided
        if branch is None:
            branch = self.get_main_branch()  
        
        contents = self.repo.get_contents('', ref=branch)
        self._download_directory(contents, save_dir, branch)
