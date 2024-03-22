# Importación de dependencias
from abc import ABC, abstractmethod

# Clase base
class BaseCommand(ABC):
    @abstractmethod
    def execute(self):# pragma: no cover
        raise NotImplementedError("Please implement in subclass")