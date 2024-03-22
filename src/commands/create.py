# Importación de dependencias
from errors.errors import ApiError, IvalidDataError, MissingToken, InvalidToken, EmailAndUuidAlreadyExist
from validators.validators import validateSchema, registerEmailSchema
from models.models import BlacklistedElement, db
from commands.base_command import BaseCommand
from sqlalchemy.exc import SQLAlchemyError
import traceback
import uuid

AUTH_TOKEN = "0536beef-b6fe-4836-86fa-88cb516874a5"

# Clase que contiene la logica de creción de usuarios
class CreateBlackList(BaseCommand):
    def __init__(self, blackList, ipaddres, headers):
        self.validateHeaders(headers)
        self.validateToken()
        self.validateRequest(blackList, ipaddres)
    
    # Función que valida los headers
    def validateHeaders(self, headers):
        if not "Authorization" in headers:
            raise MissingToken
        self.token = headers["Authorization"]
    
    # Función que valida el token
    def validateToken(self):
        if AUTH_TOKEN != self.token.replace("Bearer ", ""):
            raise InvalidToken
    
    # Función que valida el request del servicio
    def validateRequest(self, blackList, ipaddress): 
        # Validacion del request
        validateSchema(blackList, registerEmailSchema)             
        self.email = blackList['email'] 
        self.appId = blackList['appId']
        self.blockedReason = blackList['blockedReason']
        self.ipAddress = ipaddress

    # Función que valida si existe un usuario con el username
    def validateEmailAndUuid(self, email, uuid):
        userToConsult = BlacklistedElement.query.filter(BlacklistedElement.email == email, BlacklistedElement.app_uuid == uuid).first()
        if userToConsult != None:
            raise EmailAndUuidAlreadyExist

    # Función que realiza creación del registro en blacklist
    def execute(self):
        try:
            self.validateEmailAndUuid(self.email, self.appId)
            newBl = BlacklistedElement(
                id=uuid.uuid4().hex,
                email=self.email,
                app_uuid=self.appId,
                blocked_reason=self.blockedReason,
                ip_addres= self.ipAddress
            )
            db.session.add(newBl)
            db.session.commit()
            return newBl
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            raise ApiError(e)
        