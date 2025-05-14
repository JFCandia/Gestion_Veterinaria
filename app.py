import os
from flask import Flask, render_template, request, redirect, url_for
from models.models import db, Producto
from routes.routes import configurar_rutas  # Importar las rutas
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models.models import Usuario
from sqlalchemy import text  # Importar text para consultas SQL

app = Flask(__name__)

# Configuración de la clave secreta
app.secret_key = 'tu_clave_secreta_unica_y_segura'

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///veterinaria.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
db.init_app(app)

# Configurar rutas adicionales
configurar_rutas(app)

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirigir a esta vista si no está autenticado

@app.route('/')
def home():
    if current_user.is_authenticated:
        return render_template('index.html')  # Página principal si está autenticado
    else:
        return redirect(url_for('login'))  # Redirigir al login si no está autenticado

@app.route("/ventas")
def ventas_page():
    ventas = db.session.execute(
        text(
            """
            SELECT v.id, c.nombre AS cliente, p.nombre AS producto, v.cantidad, 
                   v.total, v.fecha 
            FROM ventas v
            JOIN clientes c ON v.cliente_id = c.id
            JOIN productos p ON v.producto_id = p.id
            """
        )
    ).fetchall()
    return render_template("ventas.html", ventas=ventas)

@app.route("/productos")
def productos_page():
    productos = Producto.query.all()
    return render_template("productos.html", productos=productos)



@app.route("/editar_producto/<int:producto_id>", methods=["GET", "POST"])
def editar_producto(producto_id):
    # Obtener el producto por ID
    producto = Producto.query.get_or_404(producto_id)
    if request.method == "POST":
        # Actualizar los datos del producto
        producto.nombre = request.form["nombre"]
        producto.precio = float(request.form["precio"])
        producto.cantidad = int(request.form["cantidad"])
        db.session.commit()
        return redirect(url_for("productos_page"))
    return render_template("editar_producto.html", producto=producto)

@app.route("/eliminar_producto/<int:producto_id>")
def eliminar_producto(producto_id):
    # Eliminar el producto por ID
    producto = Producto.query.get_or_404(producto_id)
    db.session.delete(producto)
    db.session.commit()
    return redirect(url_for("productos_page"))

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template('404.html'), 404

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crear las tablas en la base de datos si no existen
    app.run(debug=True)
