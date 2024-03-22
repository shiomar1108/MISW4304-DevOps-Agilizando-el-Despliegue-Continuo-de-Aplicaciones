# Importación de dependencias
from abc import ABC, abstractmethod

# Clase base
class BaseQuery(ABC):
    @abstractmethod
    def query(self): # pragma: no cover
        raise NotImplementedError("Please implement in subclass")