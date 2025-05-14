from flask import request, redirect, url_for, render_template, flash
from flask_login import login_user, logout_user, login_required, current_user
from models.models import db, Cliente, Mascota, Cita, Producto, Usuario, Venta
from datetime import datetime

def configurar_rutas(app):
    # -------------------------------
    # Rutas para Clientes
    # -------------------------------
    @app.route('/agregar_cliente', methods=['POST'])
    @login_required
    def agregar_cliente():
        nombre = request.form['nombre']
        correo = request.form['correo']
        telefono = request.form['telefono']

        nuevo_cliente = Cliente(nombre=nombre, correo=correo, telefono=telefono)
        db.session.add(nuevo_cliente)
        db.session.commit()

        return redirect(url_for('listar_clientes'))

    @app.route('/clientes')
    @login_required
    def listar_clientes():
        clientes = Cliente.query.all()
        return render_template('clientes.html', clientes=clientes)

    # -------------------------------
    # Rutas para Mascotas
    # -------------------------------
    @app.route('/agregar_mascota', methods=['POST'])
    @login_required
    def agregar_mascota():
        nombre = request.form['nombre']
        especie = request.form['especie']
        edad = request.form['edad']
        dueño_id = request.form['dueño_id']

        nueva_mascota = Mascota(nombre=nombre, especie=especie, edad=int(edad), dueño_id=int(dueño_id))
        db.session.add(nueva_mascota)
        db.session.commit()

        return redirect(url_for('listar_mascotas'))

    @app.route('/mascotas')
    @login_required
    def listar_mascotas():
        mascotas = Mascota.query.all()
        clientes = Cliente.query.all()
        return render_template('mascotas.html', mascotas=mascotas, clientes=clientes)

    # -------------------------------
    # Rutas para Citas
    # -------------------------------
    @app.route('/agregar_cita', methods=['POST'])
    @login_required
    def agregar_cita():
        fecha_str = request.form['fecha']  # Obtiene la fecha como cadena
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()  # Convierte a objeto date
        motivo = request.form['motivo']
        mascota_id = request.form['mascota_id']

        nueva_cita = Cita(fecha=fecha, motivo=motivo, mascota_id=mascota_id)
        db.session.add(nueva_cita)
        db.session.commit()

        return redirect('/citas')

    @app.route('/citas')
    @login_required
    def citas():
        citas = Cita.query.join(Mascota).all()  # Asegúrate de que las relaciones estén cargadas
        mascotas = Mascota.query.all()
        return render_template('citas.html', citas=citas, mascotas=mascotas)

    # -------------------------------
    # Rutas para Inventario
    # -------------------------------
    @app.route('/inventario')
    @login_required
    def listar_inventario():
        productos = Producto.query.all()
        return render_template('inventario.html', productos=productos)

    @app.route('/agregar_producto', methods=['POST'])
    @login_required
    def agregar_producto():
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        precio = request.form['precio']

        nuevo_producto = Producto(nombre=nombre, cantidad=int(cantidad), precio=float(precio))
        db.session.add(nuevo_producto)
        db.session.commit()

        return redirect(url_for('listar_inventario'))

    # -------------------------------
    # Rutas para Usuarios
    # -------------------------------
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('home'))  # Redirigir al home si ya está autenticado

        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']

            # Verificar si el usuario ya existe
            if Usuario.query.filter_by(email=email).first():
                flash('El correo ya está registrado.')
                return redirect(url_for('register'))

            nuevo_usuario = Usuario(username=username, email=email)
            nuevo_usuario.set_password(password)
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash('Usuario registrado con éxito. Ahora puedes iniciar sesión.')
            return redirect(url_for('login'))

        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('home'))  # Redirigir al home si ya está autenticado

        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            usuario = Usuario.query.filter_by(email=email).first()

            if usuario and usuario.check_password(password):
                login_user(usuario)
                flash('Inicio de sesión exitoso.')
                return redirect(url_for('home'))
            else:
                flash('Correo o contraseña incorrectos.')

        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Has cerrado sesión.')
        return redirect(url_for('login'))

    @app.route('/productos')
    @login_required
    def listar_productos():
        productos = Producto.query.all()
        return render_template("productos.html", productos=productos)

    @app.route('/ventas')
    @login_required
    def listar_ventas():
        ventas = db.session.execute(
            """
            SELECT v.id, c.nombre AS cliente, p.nombre AS producto, v.cantidad, 
                   v.total, v.fecha 
            FROM ventas v
            JOIN clientes c ON v.cliente_id = c.id
            JOIN productos p ON v.producto_id = p.id
            """
        ).fetchall()
        return render_template('ventas.html', ventas=ventas)

    @app.route('/agregar_venta', methods=['POST'])
    @login_required
    def agregar_venta():
        cliente_id = request.form['cliente_id']
        producto_id = request.form['producto_id']
        cantidad = int(request.form['cantidad'])

        # Obtener el precio del producto
        producto = Producto.query.get(producto_id)
        if not producto or producto.cantidad < cantidad:
            flash('No hay suficiente stock del producto.')
            return redirect(url_for('listar_ventas'))

        total = producto.precio * cantidad

        # Crear la nueva venta
        nueva_venta = Venta(cliente_id=cliente_id, producto_id=producto_id, cantidad=cantidad, total=total, fecha=datetime.now())
        db.session.add(nueva_venta)

        # Actualizar el stock del producto
        producto.cantidad -= cantidad
        db.session.commit()

        flash('Venta registrada con éxito.')
        return redirect(url_for('listar_ventas'))
