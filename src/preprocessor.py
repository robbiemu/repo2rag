import os
from typing import Dict

from preprocessor_plugin import PreprocessorPlugin
from preprocessors.pdf import PDFPreprocessor


PLUGINS = [PDFPreprocessor]

class Preprocessor:
    """A preprocessor is a class that can extract text from a file."""
    def __init__(self, without_plugins: bool):
        self.plugins: Dict[str, PreprocessorPlugin] = {}

        if without_plugins:
            return
        for plugin_klass in PLUGINS:
            plugin = plugin_klass()
            for extension in plugin.get_supported_extensions():
                self.register_plugin(extension, plugin)

    def register_plugin(self, extension: str, 
                        plugin: PreprocessorPlugin) -> None:
        self.plugins[extension] = plugin

    def preprocess_file(self, file_path: str) -> str:
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        if ext in self.plugins:
            plugin = self.plugins[ext]
            return plugin.extract_text(file_path)
        else:
            return self.default_text_extractor(file_path)

    @staticmethod
    def default_text_extractor(file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
