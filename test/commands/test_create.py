from src.commands.create import CreateBlackList
from src.errors.errors import EmailAndUuidAlreadyExist, InvalidToken, MissingToken
from faker import Faker
import uuid
import random
import src.application

# Clase que contiene la logica de las pruebas del servicio
class TestCreate():
    # Declaración constantes
    dataFactory = Faker()
    listBlockedReason = [
        "El dominio del envío es se encuentra bloquedo en su organización",
        "Se bloquea por considerarse email que envia SPAM o correos basura",
        "Intento de suplantación de identidad realizado con el nombre para mostrar"
        "El idioma del email está en la lista de bloqueados de su organización",
        "La dirección IP o el rango están en la lista de bloqueados de su organización",
        "El país desde el cual se envió el email está bloqueado por su organización"
    ]
    email = None
    appId = None
    blockedReason = None
    ipaddress = None
    data = {}
    headers = {}
    token = "0536beef-b6fe-4836-86fa-88cb516874a5"

    # Función que genera data del usuario
    def set_up(self):
        self.email = self.dataFactory.email()
        self.appId = uuid.uuid4().hex
        self.blockedReason = random.choice(self.listBlockedReason)
        self.ipaddress = self.dataFactory.ipv4()
        self.data = {
            "email": f"{self.email}",
            "appId": f"{self.appId}",
            "blockedReason": f"{self.blockedReason}"
        }
        self.headers["Authorization"] = f"Bearer {self.token}"
            
    # Función que valida el registro exitoso de un email en listas negras
    def test_register_email_in_blacklist(self):
        # Creación usuario
        self.set_up()
        result = CreateBlackList(self.data, self.ipaddress, self.headers).execute()
        assert result != None
        assert result.email == self.email
        assert result.app_uuid == self.appId
        assert result.blocked_reason == self.blockedReason
        assert result.ip_addres == self.ipaddress
        assert result.createdAt != None
    
    # Función que valida que no se pueda registrar el mismo email y appId más de una vez
    def test_register_existing_email_in_blaklist(self):
        try:
            # Creación usuario
            self.set_up()
            result = CreateBlackList(self.data, self.ipaddress, self.headers).execute()
            assert result != None
            # Creación usuario existente
            result = CreateBlackList(self.data, self.ipaddress, self.headers).execute()
        except Exception as e:
            assert e.code == EmailAndUuidAlreadyExist.code
            assert e.description == EmailAndUuidAlreadyExist.description

    # Función que valida que el token recibido sea valido
    def test_validate_invalid_token(self):
        try:
            self.set_up()
            invalidToken = "4950f94e-7478-11ee-b962-0242ac120002"
            self.headers["Authorization"] = f"Bearer {invalidToken}"
            result = CreateBlackList(self.data, self.ipaddress, self.headers).execute()
        except Exception as e:
            assert e.code == InvalidToken.code
            assert e.description == InvalidToken.description

    # Función que valida que el token venga en los headers
    def test_validate_missing_token(self):
        try:
            self.set_up()
            headers = {}
            result = CreateBlackList(self.data, self.ipaddress, headers).execute()
        except Exception as e:
            assert e.code == MissingToken.code
            assert e.description == MissingToken.description               