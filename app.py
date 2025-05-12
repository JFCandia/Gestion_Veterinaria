from flask import Flask, render_template, send_from_directory
from models.models import db
from routes.routes import configurar_rutas  # Importar las rutas



app = Flask(__name__)
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
