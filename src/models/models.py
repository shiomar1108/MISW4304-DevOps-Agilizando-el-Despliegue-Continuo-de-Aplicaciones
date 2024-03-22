# Importación de dependencias
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID

# Creación de variable db
db = SQLAlchemy()

# Clase que cotiene la definición del modelo de base de datos
class BlacklistedElement(db.Model):
    __tablename__ = "blacklist"
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    email = db.Column(db.String(256), nullable=True)
    app_uuid = db.Column(db.String(256), nullable=True)
    blocked_reason = db.Column(db.String(256), nullable=True)
    ip_addres = db.Column(db.String(256), nullable=True)
    createdAt = db.Column(DateTime, default=datetime.utcnow)

class BlacklistedElementSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = BlacklistedElement
        id = fields.String()