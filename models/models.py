from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Modelo de Cliente
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    mascotas = db.relationship('Mascota', backref='dueño', lazy=True)

# Modelo de Mascota
class Mascota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(50), nullable=False)
    edad = db.Column(db.Integer)
    dueño_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)

# Modelo de Cita
class Cita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(20), nullable=False)
    motivo = db.Column(db.String(200))
    mascota_id = db.Column(db.Integer, db.ForeignKey('mascota.id'), nullable=False)

# Modelo de Inventario (medicamentos y productos)
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)