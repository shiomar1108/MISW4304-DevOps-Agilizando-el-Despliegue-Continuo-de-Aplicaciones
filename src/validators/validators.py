# Importación de dependencias
from errors.errors import BadRequest
from jsonschema import validate
import jsonschema
import traceback

# Esquema para el registro de email en listas negras
registerEmailSchema = {
    "type": "object",
    "properties": {
        "email": {"type": "string", "minimum": 6, "maximum": 64, "format": "email"},
        "appId":  {"type": "string", "minimum": 6, "maximum": 32},
        "blockedReason":  {"type": "string", "minimum": 6, "maximum": 256}
    },
    "required": ["email", "appId", "blockedReason"]
}

# Función que valida el request para la creación de publicacion
def validateSchema(jsonData, schema):
    try:
        validate(instance=jsonData, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        traceback.print_exc()
        raise BadRequest