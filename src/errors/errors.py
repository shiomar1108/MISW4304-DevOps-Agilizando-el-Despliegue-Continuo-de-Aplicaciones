# Clase que contiene la estructura de error por defecto
class ApiError(Exception):
    code = 500
    description = "Error interno, por favor revise el log"


# Clase que contiene la estructura de error por defecto
class AuthError(Exception):
    code = 401
    description = "Token Invalido"

# Clase que contiene la estructura de error cuando no se envia el token
class MissingToken(ApiError):
    code = 403
    description = "El token no está en el encabezado de la solicitud"

# Clase que contiene la estructura de error por defecto
class IvalidDataError(Exception):
    code = 409
    description = "Datos de Entrada invalidos"

# Clase que contiene la estructura de error cuando el token no es valido o esta vencido
class InvalidToken(ApiError):
    code = 401
    description = "El token no es válido"     
    
# Clase que contiene la estructura de error cuando no esta registra el username
class EmailAndUuidAlreadyExist(ApiError):
    code = 409
    description = "El email y la aplicación ya se encuentran registradas"    

# Clase que contiene la estructura de un error de tipo Bad Request
class BadRequest(ApiError):
    code = 400
    description = "Párametros de entrada invalidos"    