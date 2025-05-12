from flask import request, redirect, url_for, render_template
from models.models import db, Cliente, Mascota, Cita, Producto

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

    # Ruta para listar clientes
    @app.route('/clientes')
    def listar_clientes():
        clientes = Cliente.query.all()
        return render_template('clientes.html', clientes=clientes)

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
    def listar_mascotas():
        mascotas = Mascota.query.all()
        clientes = Cliente.query.all()
        return render_template('mascotas.html', mascotas=mascotas, clientes=clientes)

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
    def listar_citas():
        citas = Cita.query.all()
        mascotas = Mascota.query.all()
        return render_template('citas.html', citas=citas, mascotas=mascotas)

    # Agregar rutas para el inventario
    @app.route('/inventario')
    def listar_inventario():
        productos = Producto.query.all()
        return render_template('inventario.html', productos=productos)

    @app.route('/agregar_producto', methods=['POST'])
    def agregar_producto():
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        precio = request.form['precio']

        nuevo_producto = Producto(nombre=nombre, cantidad=int(cantidad), precio=float(precio))
        db.session.add(nuevo_producto)
        db.session.commit()

        return redirect(url_for('listar_inventario'))
