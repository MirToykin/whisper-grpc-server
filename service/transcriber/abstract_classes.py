from abc import ABC, abstractmethod


class Transcriber(ABC):
    @abstractmethod
    def transcribe_by_path(self, path: str, lang: str = None) -> str:
        pass

    @abstractmethod
    def transcribe_by_binary(self, audio_data: bytes, lang: str = None) -> str:
        pass
