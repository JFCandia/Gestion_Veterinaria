from flask import request, redirect, url_for, render_template, flash
from flask_login import login_user, logout_user, login_required
from models.models import db, Cliente, Mascota, Cita, Producto, Usuario

def configurar_rutas(app):
    # Ruta para agregar cliente
    @app.route('/agregar_cliente', methods=['POST'])
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
        # Obtener el término de búsqueda desde los parámetros de la URL
        search = request.args.get('search', '', type=str)
        page = request.args.get('page', 1, type=int)

        # Filtrar clientes si hay un término de búsqueda
        if search:
            clientes = Cliente.query.filter(
                Cliente.nombre.ilike(f'%{search}%') |
                Cliente.correo.ilike(f'%{search}%') |
                Cliente.telefono.ilike(f'%{search}%')
            ).paginate(page=page, per_page=5)
        else:
            # Mostrar todos los clientes si no hay búsqueda
            clientes = Cliente.query.paginate(page=page, per_page=5)

        return render_template('clientes.html', clientes=clientes, search=search)

    # Ruta para agregar mascota
    @app.route('/agregar_mascota', methods=['POST'])
    def agregar_mascota():
        nombre = request.form['nombre']
        especie = request.form['especie']
        edad = request.form['edad']
        dueño_id = request.form['dueño_id']

        nueva_mascota = Mascota(nombre=nombre, especie=especie, edad=int(edad), dueño_id=int(dueño_id))
        db.session.add(nueva_mascota)
        db.session.commit()

        return redirect(url_for('listar_mascotas'))

    # Ruta para listar mascotas
    @app.route('/mascotas')
    @login_required
    def listar_mascotas():
        search = request.args.get('search', '', type=str)
        page = request.args.get('page', 1, type=int)

        if search:
            mascotas = Mascota.query.filter(
                Mascota.nombre.ilike(f'%{search}%') |
                Mascota.especie.ilike(f'%{search}%')
            ).paginate(page=page, per_page=5)
        else:
            mascotas = Mascota.query.paginate(page=page, per_page=5)

        clientes = Cliente.query.all()  # Para el formulario de agregar mascota
        return render_template('mascotas.html', mascotas=mascotas, clientes=clientes, search=search)

    # Ruta para agregar cita
    @app.route('/agregar_cita', methods=['POST'])
    def agregar_cita():
        fecha = request.form['fecha']
        motivo = request.form['motivo']
        mascota_id = request.form['mascota_id']

        nueva_cita = Cita(fecha=fecha, motivo=motivo, mascota_id=int(mascota_id))
        db.session.add(nueva_cita)
        db.session.commit()

        return redirect(url_for('listar_citas'))

    # Ruta para listar citas
    @app.route('/citas')
    @login_required
    def listar_citas():
        search = request.args.get('search', '', type=str)
        page = request.args.get('page', 1, type=int)

        if search:
            citas = Cita.query.filter(
                Cita.motivo.ilike(f'%{search}%')
            ).paginate(page=page, per_page=5)
        else:
            citas = Cita.query.paginate(page=page, per_page=5)

        mascotas = Mascota.query.all()  # Para el formulario de agregar cita
        return render_template('citas.html', citas=citas, mascotas=mascotas, search=search)

    # Agregar rutas para el inventario
    @app.route('/inventario')
    @login_required
    def listar_inventario():
        search = request.args.get('search', '', type=str)
        page = request.args.get('page', 1, type=int)

        if search:
            productos = Producto.query.filter(
                Producto.nombre.ilike(f'%{search}%')
            ).paginate(page=page, per_page=5)
        else:
            productos = Producto.query.paginate(page=page, per_page=5)

        return render_template('inventario.html', productos=productos, search=search)

    @app.route('/agregar_producto', methods=['POST'])
    def agregar_producto():
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        precio = request.form['precio']

        nuevo_producto = Producto(nombre=nombre, cantidad=int(cantidad), precio=float(precio))
        db.session.add(nuevo_producto)
        db.session.commit()

        return redirect(url_for('listar_inventario'))

    # Ruta para registrar usuarios
    @app.route('/register', methods=['GET', 'POST'])
    def register():
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

    # Ruta para iniciar sesión
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            usuario = Usuario.query.filter_by(email=email).first()

            if usuario and usuario.check_password(password):
                login_user(usuario)
                flash('Inicio de sesión exitoso.')
                next_page = request.args.get('next')  # Redirige a la página solicitada o al index
                return redirect(next_page or url_for('home'))
            else:
                flash('Correo o contraseña incorrectos.')

        return render_template('login.html')

    # Ruta para cerrar sesión
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Has cerrado sesión.')
        return redirect(url_for('login'))
