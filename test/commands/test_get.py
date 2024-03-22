from src.queries.get import isBlackListed
from src.commands.create import CreateBlackList
from src.errors.errors import InvalidToken, MissingToken
from faker import Faker
import uuid
import random
import src.application

# Clase que contiene la logica de las pruebas de consulta del servicio
class TestGet():
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
        
    # Función que valida que un email no se encuentre en listas negras
    def test_get_email_not_in_blacklist(self):
        # consulta email
        self.set_up()
        self.email='bc@abc.com'
        result = isBlackListed(self.email, self.headers).query()
        print(result)
        assert result != None
        assert result['isblocked'] == False
        assert result['blocked_reason'] == 'N/A'

    # Función que valida que un email se encuentre en listas negras
    def test_get_email_in_blacklist(self):
        # Registro de email
        self.set_up()
        CreateBlackList(self.data, self.ipaddress, self.headers).execute()
        # Consulta email
        result = isBlackListed(self.email, self.headers).query()
        print(result)
        assert result != None
        assert result['isblocked'] == True
        assert result['blocked_reason'] == self.blockedReason

    # Función que valida que el token recibido sea valido
    def test_validate_invalid_token(self):
        try:
            self.set_up()
            invalidToken = "4950f94e-7478-11ee-b962-0242ac120002"
            self.headers["Authorization"] = f"Bearer {invalidToken}"
            isBlackListed(self.email, self.headers).query()
        except Exception as e:
            assert e.code == InvalidToken.code
            assert e.description == InvalidToken.description

    # Función que valida que el token venga en los headers
    def test_validate_missing_token(self):
        try:
            self.set_up()
            headers = {}
            isBlackListed(self.email, headers).query()
        except Exception as e:
            assert e.code == MissingToken.code
            assert e.description == MissingToken.description  