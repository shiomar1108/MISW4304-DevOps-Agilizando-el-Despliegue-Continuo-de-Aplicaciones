# Importación de dependencias
from queries.base_query import BaseQuery
from models.models import BlacklistedElement
from sqlalchemy.exc import SQLAlchemyError
from errors.errors import ApiError, MissingToken, InvalidToken
import logging

# Constantes
LOG = "[Get blacklisted email]"
AUTH_TOKEN = "0536beef-b6fe-4836-86fa-88cb516874a5"

# Clase que contiene la logica de consulta de usuarios
class isBlackListed(BaseQuery):
    def __init__(self, email, headers):
        self.validateHeaders(headers)
        self.validateToken()
        self.email = email

    # Función que valida los headers
    def validateHeaders(self, headers):
        if not "Authorization" in headers:
            raise MissingToken
        self.token = headers["Authorization"]
    
    # Función que valida el token
    def validateToken(self):
        if AUTH_TOKEN != self.token.replace("Bearer ", ""):
            raise InvalidToken

    # Función que realiza consulta de usuarios
    def query(self):
        try:
            response = {'isblocked': False, 'blocked_reason': 'N/A'}
            email_element = BlacklistedElement.query.filter(BlacklistedElement.email == self.email).first()
            if email_element != None:
                response = {'isblocked': True, 'blocked_reason': email_element.blocked_reason}
            return response
            
        except SQLAlchemyError as e:# pragma: no cover
            logging.error(e)
            raise ApiError(e)