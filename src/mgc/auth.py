from abc import ABC, abstractmethod


class AuthProvider(ABC):

    @abstractmethod
    def get_access_token(self) -> str:
        raise NotImplementedError