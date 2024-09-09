from typing import Set


class PreprocessorPlugin:
    # abstract class
    @staticmethod
    def get_supported_extensions() -> Set[str]:
        """Return a set of file extensions supported by this plugin."""
        raise NotImplementedError(
            "Plugin must implement get_supported_extensions")

    def extract_text(self, file_path: str) -> str:
        raise NotImplementedError("Preprocessor must implement extract_text")
