import os
from flask import Flask, render_template, send_from_directory
from models.models import db
from routes.routes import configurar_rutas  # Importar las rutas
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models.models import Usuario

app = Flask(__name__)

# Configuración de la clave secreta
app.secret_key = 'tu_clave_secreta_unica_y_segura'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///veterinaria.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
configurar_rutas(app)  # Aquí conectamos las rutas con la aplicación

@app.route('/')
def home():
    return render_template('index.html')


@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template('404.html'), 404

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirigir a esta vista si no está autenticado

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

if __name__ == '__main__': 
    with app.app_context():
        db.create_all()
    app.run(debug=True)
