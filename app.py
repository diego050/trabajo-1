from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from faker import Faker
from sqlalchemy import UniqueConstraint
from datetime import datetime, timedelta
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = "helloworld"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:1234@localhost:5432/base_datos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
fake = Faker()

# Tabla de HOTEL pero en tercera forma:
class telefonoHotel(db.Model):
    id_telefono = db.Column(db.Integer, primary_key=True)
    id_hotel = db.Column(db.Integer, db.ForeignKey('hotel.id_hotel'))
    telefono_hotel = db.Column(db.String(50), nullable=False)

class hotel(db.Model):
    id_hotel = db.Column(db.Integer, primary_key=True)
    id_distrito = db.Column(db.Integer, db.ForeignKey('distrito.id_distrito'), nullable=False)
    n_habitaciones = db.Column(db.Integer)
    n_estrellas = db.Column(db.Integer)

class distrito(db.Model):
    id_distrito = db.Column(db.Integer, primary_key=True)
    nombre_distrito = db.Column(db.String(50), nullable=False)

#tabla de PERSONAL en tercera forma:
class tipo_trabajo(db.Model):
    id_tipo = db.Column(db.Integer, primary_key=True)
    nombre_tipo = db.Column(db.String(150), nullable=False)

class personal(db.Model):
    dni_personal = db.Column(db.String(50), primary_key=True)
    nombre_personal = db.Column(db.String(50))
    apellido_personal = db.Column(db.String(50))
    sueldo = db.Column(db.Integer)
    fecha_contratacion = (db.Date)
    id_tipo = db.Column(db.Integer, db.ForeignKey('tipo_trabajo.id_tipo'), nullable=False)

#relacion trabaja
class trabaja(db.Model):
    id_hotel = db.Column(db.Integer, db.ForeignKey('hotel.id_hotel'), nullable=False, primary_key=True)
    dni_personal = db.Column(db.String(50), db.ForeignKey('personal.dni_personal'), nullable=False, primary_key=True)

#tabla de Asistencia en tercera forma:
class asistencia(db.Model):
    id_asistencia = db.Column(db.Integer, primary_key=True)
    fecha_asistencia = db.Column(db.Date)
    hora_llegada = db.Column(db.Time)
    hora_salida = db.Column(db.Time)
    dni_personal = db.Column(db.String(50), db.ForeignKey('personal.dni_personal'), nullable=False)

#tabla Servicio en tercera forma:
class servicio(db.Model):
    id_servicio = db.Column(db.Integer, primary_key=True)
    nombre_servicio = db.Column(db.String(50))
    precio = db.Column(db.Integer)

#relacion labora
class labora(db.Model):
    id_servicio = db.Column(db.Integer, db.ForeignKey('servicio.id_servicio'), nullable=False, primary_key=True)
    dni_personal = db.Column(db.String(50), db.ForeignKey('personal.dni_personal'), nullable=False, primary_key=True)

#relacion ofrece
class ofrece(db.Model):
    fecha_asistencia = db.Column(db.Date)
    hora_llegada = db.Column(db.Time)
    id_servicio = db.Column(db.Integer, db.ForeignKey('servicio.id_servicio'), nullable=False, primary_key=True)
    id_hotel = db.Column(db.Integer, db.ForeignKey('hotel.id_hotel'), nullable=False, primary_key=True)

#tabla clientes
class cliente(db.Model):
    dni_cliente = db.Column(db.String(50), primary_key=True)
    edad = db.Column(db.Integer)
    nombre = db.Column(db.String(50))
    apellido = db.Column(db.String(50))
    telefono_cliente = db.Column(db.String(50))
    email_cliente = db.Column(db.String(50))
    contraseña_cliente = db.Column(db.String(50))

#relacion pide
class pide(db.Model):
    id_servicio = db.Column(db.Integer, db.ForeignKey('servicio.id_servicio'), nullable=False, primary_key=True)
    dni_cliente = db.Column(db.String(50), db.ForeignKey('cliente.dni_cliente'), nullable=False, primary_key=True)

#tabla acompañante
class acompañante(db.Model):
    dni_acompañante = db.Column(db.String(50), primary_key=True)
    dni_cliente = db.Column(db.String(50), db.ForeignKey('cliente.dni_cliente'), nullable=False)
    nombre_acompañante = db.Column(db.String(50))
    apellido_acompañante = db.Column(db.String(50))
    edad = db.Column(db.String(50))

#relacion hospeda
class hospedaje(db.Model):
    dni_cliente = db.Column(db.String(50), db.ForeignKey('cliente.dni_cliente'), nullable=False, primary_key=True)
    dni_acompañante = db.Column(db.String(50), db.ForeignKey('acompañante.dni_acompañante'), nullable=False, primary_key=True)
    id_hotel = db.Column(db.Integer, db.ForeignKey('hotel.id_hotel'), nullable=False, primary_key=True)

#tabla calificacion
class calificacion(db.Model):
    puntuacion = db.Column(db.Integer)
    reseña = db.Column(db.String(150))
    dni_cliente = db.Column(db.String(50), db.ForeignKey('cliente.dni_cliente'), primary_key=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id_hotel'), primary_key=True)

#tabla Habitacion normalizada
class tipohabitacion(db.Model):
    id_tipo_hab = db.Column(db.Integer, primary_key=True)
    tipo_habitacion = db.Column(db.String(50))
    n_camas_habitacion = db.Column(db.Integer)
    precio_habitacion = db.Column(db.Integer)

class habitacion(db.Model):
    __table_args__ = (UniqueConstraint('id_hotel', 'num_habitacion', name='unique_hotel_room'),)

    id_habitacion = db.Column(db.Integer, nullable=False, primary_key=True)
    id_hotel = db.Column(db.Integer, db.ForeignKey('hotel.id_hotel'), nullable=False)
    num_habitacion = db.Column(db.Integer, nullable=False)
    id_tipo_hab = db.Column(db.Integer, db.ForeignKey('tipohabitacion.id_tipo_hab'), nullable=False)
    disponibilidad_habitacion = db.relationship('disponibilidad', backref='habitacion', lazy=True)
    
class disponibilidad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_habitacion = db.Column(db.Integer, db.ForeignKey('habitacion.id_habitacion'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    disponible = db.Column(db.Boolean, default=True)

#tabla empresa
class empresa(db.Model):
    ruc_empresa = db.Column(db.String(50), primary_key=True)
    nombre = db.Column(db.String(50))
    email = db.Column(db.String(50))
    telefono = db.Column(db.String(50))

#tabla producto
class producto(db.Model):
    id_producto = db.Column(db.Integer, primary_key=True)
    nombre_producto = db.Column(db.String(50))
    descripcion = db.Column(db.String(150))

#relacion comercializa
class comercializa(db.Model):
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id_producto'), nullable=False, primary_key=True)
    ruc = db.Column(db.String(50), db.ForeignKey('empresa.ruc_empresa'), nullable=False, primary_key=True)

#relacion provee
class provee(db.Model):
    fecha_entrega = db.Column(db.Date)
    id_hotel = db.Column(db.Integer, db.ForeignKey('hotel.id_hotel'), nullable=False, primary_key=True)
    ruc = db.Column(db.String(50), db.ForeignKey('empresa.ruc_empresa'), nullable=False, primary_key=True)

#tabla reservacion
class reservacion(db.Model):
    id_habitacion = db.Column (db.Integer, db.ForeignKey('habitacion.id_habitacion'), nullable=False, primary_key=True)
    dni_cliente = db.Column(db.String(50), db.ForeignKey('cliente.dni_cliente'), nullable=False, primary_key=True)
    fecha_reservada = db.Column (db.Date, nullable=False, primary_key=True)

#crea datos falsos
def create_fake_data():
    for a in range(5):
        new_distrito = distrito(
            nombre_distrito=fake.city() + ' District'
        )
        db.session.add(new_distrito)
    
    db.session.commit()
    for a in range(5):
        new_hotel = hotel(
            id_distrito=new_distrito.id_distrito,
            n_habitaciones=fake.random_int(min=10, max=100),
            n_estrellas=fake.random_int(min=1, max=5)
        )
        db.session.add(new_hotel)
    db.session.commit()

    for a in range(5):
        new_telefono = telefonoHotel(
            id_hotel=new_hotel.id_hotel,
            telefono_hotel=fake.phone_number()
        )
        db.session.add(new_telefono)
    db.session.commit()
    
    for a in range(10):
        new_tipo_trabajo = tipo_trabajo(
            nombre_tipo=fake.job()
        )
        db.session.add(new_tipo_trabajo)
    db.session.commit()

    for a in range(20):
        new_personal = personal(
            dni_personal=fake.unique.random_number(digits=8),
            nombre_personal=fake.first_name(),
            apellido_personal=fake.last_name(),
            sueldo=fake.random_int(min=20000, max=80000),
            fecha_contratacion=fake.date_between(start_date='-5y', end_date='today'),
            id_tipo=fake.random_int(min=1, max=10)  # Asociamos a uno de los 10 tipos de trabajo
        )
        db.session.add(new_personal)
    db.session.commit()

    for a in range(15):
        # Selecciona un hotel y un trabajador de manera aleatoria
        random_hotel = hotel.query.order_by(func.random()).first()
        random_personal = personal.query.order_by(func.random()).first()

        # Verificar si la asociación ya existe
        asociacion_existente = trabaja.query.filter_by(
            id_hotel=random_hotel.id_hotel,
            dni_personal=random_personal.dni_personal
        ).first()

        # Si la asociación no existe, crea una nueva
        if not asociacion_existente:
            nueva_asociacion = trabaja(
                id_hotel=random_hotel.id_hotel,
                dni_personal=random_personal.dni_personal
            )
        db.session.add(nueva_asociacion)
    db.session.commit()

    for a in range(30):
        # Selecciona un trabajador de manera aleatoria
        random_personal = personal.query.order_by(func.random()).first()

        # Genera fechas y horas aleatorias
        fecha_asistencia = fake.date_between(start_date='-1y', end_date='today')
        hora_llegada = fake.time(pattern='%H:%M:%S')
        hora_salida = fake.time(pattern='%H:%M:%S')

        # Crea una nueva entrada de asistencia
        nueva_asistencia = asistencia(
            fecha_asistencia=fecha_asistencia,
            hora_llegada=hora_llegada,
            hora_salida=hora_salida,
            dni_personal=random_personal.dni_personal
        )

        db.session.add(nueva_asistencia)
    db.session.commit()

    for a in range(15):
        # Genera nombres de servicios y precios aleatorios
        nombre_servicio = fake.word()
        precio = fake.random_int(min=5, max=100)

        # Crea un nuevo servicio
        nuevo_servicio = servicio(
            nombre_servicio=nombre_servicio,
            precio=precio
        )

        db.session.add(nuevo_servicio)
    db.session.commit()

    for a in range(15):
        # Selecciona un servicio y personal de manera aleatoria
        random_servicio = servicio.query.order_by(func.random()).first()
        random_personal = personal.query.order_by(func.random()).first()

        # Verificar si la asociación ya existe
        asociacion_existente = labora.query.filter_by(
            id_servicio=random_servicio.id_servicio,
            dni_personal=random_personal.dni_personal
        ).first()

        # Si la asociación no existe, crea una nueva
        if not asociacion_existente:
            nueva_asociacion = labora(
                id_servicio=random_servicio.id_servicio,
                dni_personal=random_personal.dni_personal
            )
        db.session.add(nueva_asociacion)
    db.session.commit()

    for a in range(20):
        # Selecciona un servicio, un hotel y una fecha aleatoria
        random_servicio = servicio.query.order_by(func.random()).first()
        random_hotel = hotel.query.order_by(func.random()).first()
        fecha_asistencia = fake.date_between(start_date='-1y', end_date='today')

        # Verifica si la asociación ya existe
        asociacion_existente = ofrece.query.filter_by(
            id_servicio=random_servicio.id_servicio,
            id_hotel=random_hotel.id_hotel
        ).first()

        # Si la asociación no existe, crea una nueva
        if not asociacion_existente:
            nueva_asociacion = ofrece(
                fecha_asistencia=fecha_asistencia,
                hora_llegada=fake.time(pattern='%H:%M:%S'),
                id_servicio=random_servicio.id_servicio,
                id_hotel=random_hotel.id_hotel
            )
            db.session.add(nueva_asociacion)
    db.session.commit()

    for a in range(15):
        # Genera datos aleatorios para el cliente
        dni_cliente = fake.unique.random_number(digits=8)
        edad = fake.random_int(min=18, max=80)
        nombre = fake.first_name()
        apellido = fake.last_name()
        telefono_cliente = fake.phone_number()
        email_cliente = fake.email()
        contraseña_cliente = fake.password()

        # Crea un nuevo cliente
        nuevo_cliente = cliente(
            dni_cliente=dni_cliente,
            edad=edad,
            nombre=nombre,
            apellido=apellido,
            telefono_cliente=telefono_cliente,
            email_cliente=email_cliente,
            contraseña_cliente=contraseña_cliente
        )

        db.session.add(nuevo_cliente)
    db.session.commit()

    for a in range(20):
        # Selecciona un servicio y un cliente de manera aleatoria
        random_servicio = servicio.query.order_by(func.random()).first()
        random_cliente = cliente.query.order_by(func.random()).first()

        # Verifica si la asociación ya existe
        asociacion_existente = pide.query.filter_by(
            id_servicio=random_servicio.id_servicio,
            dni_cliente=random_cliente.dni_cliente
        ).first()

        # Si la asociación no existe, crea una nueva
        if not asociacion_existente:
            nueva_asociacion = pide(
                id_servicio=random_servicio.id_servicio,
                dni_cliente=random_cliente.dni_cliente
            )
            db.session.add(nueva_asociacion)
    db.session.commit()

    for a in range(15):
        # Selecciona un cliente de manera aleatoria
        random_cliente = cliente.query.order_by(func.random()).first()

        # Genera datos aleatorios para el acompañante
        dni_acompañante = fake.unique.random_number(digits=8)
        nombre_acompañante = fake.first_name()
        apellido_acompañante = fake.last_name()
        edad_acompañante = fake.random_int(min=18, max=80)

        # Crea un nuevo acompañante
        nuevo_acompañante = acompañante(
            dni_acompañante=dni_acompañante,
            dni_cliente=random_cliente.dni_cliente,
            nombre_acompañante=nombre_acompañante,
            apellido_acompañante=apellido_acompañante,
            edad=edad_acompañante
        )

        db.session.add(nuevo_acompañante)
    db.session.commit()

    for a in range(20):
        # Selecciona un cliente, un acompañante y un hotel de manera aleatoria
        random_cliente = cliente.query.order_by(func.random()).first()
        random_acompañante = acompañante.query.order_by(func.random()).first()
        random_hotel = hotel.query.order_by(func.random()).first()

        # Verifica si el hospedaje ya existe
        hospedaje_existente = hospedaje.query.filter_by(
            dni_cliente=random_cliente.dni_cliente,
            dni_acompañante=random_acompañante.dni_acompañante,
            id_hotel=random_hotel.id_hotel
        ).first()

        # Si el hospedaje no existe, crea uno nuevo
        if not hospedaje_existente:
            nuevo_hospedaje = hospedaje(
                dni_cliente=random_cliente.dni_cliente,
                dni_acompañante=random_acompañante.dni_acompañante,
                id_hotel=random_hotel.id_hotel
            )
            db.session.add(nuevo_hospedaje)
    db.session.commit()

    for a in range(20):
        # Selecciona un cliente, un acompañante y un hotel de manera aleatoria
        random_cliente = cliente.query.order_by(func.random()).first()
        random_acompañante = acompañante.query.order_by(func.random()).first()
        random_hotel = hotel.query.order_by(func.random()).first()

        # Verifica si el hospedaje ya existe
        hospedaje_existente = hospedaje.query.filter_by(
            dni_cliente=random_cliente.dni_cliente,
            dni_acompañante=random_acompañante.dni_acompañante,
            id_hotel=random_hotel.id_hotel
        ).first()

        # Si el hospedaje no existe, crea uno nuevo
        if not hospedaje_existente:
            nuevo_hospedaje = hospedaje(
                dni_cliente=random_cliente.dni_cliente,
                dni_acompañante=random_acompañante.dni_acompañante,
                id_hotel=random_hotel.id_hotel
            )
            db.session.add(nuevo_hospedaje)
    db.session.commit()

    for a in range(15):
        # Selecciona un cliente y un hotel de manera aleatoria
        random_cliente = cliente.query.order_by(func.random()).first()
        random_hotel = hotel.query.order_by(func.random()).first()

        # Verifica si la calificación ya existe
        calificacion_existente = calificacion.query.filter_by(
            dni_cliente=random_cliente.dni_cliente,
            hotel_id=random_hotel.id_hotel
        ).first()

        # Si la calificación no existe, crea una nueva
        if not calificacion_existente:
            nueva_calificacion = calificacion(
                puntuacion=fake.random_int(min=1, max=5),
                reseña=fake.text(max_nb_chars=150),
                dni_cliente=random_cliente.dni_cliente,
                hotel_id=random_hotel.id_hotel
            )
            db.session.add(nueva_calificacion)
    db.session.commit()

    for a in range(10):
        # Genera datos aleatorios para el tipo de habitación
        tipo_habitacion = fake.word()
        n_camas_habitacion = fake.random_int(min=1, max=4)
        precio_habitacion = fake.random_int(min=50, max=300)

        # Crea un nuevo tipo de habitación
        nuevo_tipo_habitacion = tipohabitacion(
            tipo_habitacion=tipo_habitacion,
            n_camas_habitacion=n_camas_habitacion,
            precio_habitacion=precio_habitacion
        )

        db.session.add(nuevo_tipo_habitacion)
    db.session.commit()

    for a in range(30):
        # Selecciona un hotel y un tipo de habitación de manera aleatoria
        random_hotel = hotel.query.order_by(func.random()).first()
        random_tipo_habitacion = tipohabitacion.query.order_by(func.random()).first()
        random_num_habitacion = fake.random_int(min=100, max=999)

        # Verifica si la habitación ya existe para ese hotel y tipo
        habitacion_existente = habitacion.query.filter_by(
            id_hotel=random_hotel.id_hotel,
            num_habitacion=random_num_habitacion
        ).first()


        # Si la habitación no existe, crea una nueva
        if not habitacion_existente:
            nueva_habitacion = habitacion(
                num_habitacion=random_num_habitacion,
                id_hotel=random_hotel.id_hotel,
                id_tipo_hab=random_tipo_habitacion.id_tipo_hab,
            )
            db.session.add(nueva_habitacion)
    db.session.commit()

    for a in range(5):
        # Genera datos aleatorios para la empresa
        ruc_empresa = fake.unique.random_number(digits=11)
        nombre_empresa = fake.company()
        email_empresa = fake.company_email()
        telefono_empresa = fake.phone_number()

        # Crea una nueva empresa
        nueva_empresa = empresa(
            ruc_empresa=ruc_empresa,
            nombre=nombre_empresa,
            email=email_empresa,
            telefono=telefono_empresa
        )

        db.session.add(nueva_empresa)
    db.session.commit()

    for a in range(15):
        # Genera datos aleatorios para el producto
        nombre_producto = fake.word()
        descripcion_producto = fake.text(max_nb_chars=150)

        # Crea un nuevo producto
        nuevo_producto = producto(
            nombre_producto=nombre_producto,
            descripcion=descripcion_producto
        )

        db.session.add(nuevo_producto)
    db.session.commit()

    for a in range(15):
        # Genera datos aleatorios para el producto
        nombre_producto = fake.word()
        descripcion_producto = fake.text(max_nb_chars=150)

        # Crea un nuevo producto
        nuevo_producto = producto(
            nombre_producto=nombre_producto,
            descripcion=descripcion_producto
        )

        db.session.add(nuevo_producto)
    db.session.commit()

    for a in range(20):
        # Selecciona un producto y una empresa de manera aleatoria
        random_producto = producto.query.order_by(func.random()).first()
        random_empresa = empresa.query.order_by(func.random()).first()

        # Verifica si la relación de comercialización ya existe
        comercializa_existente = comercializa.query.filter_by(
            id_producto=random_producto.id_producto,
            ruc=random_empresa.ruc_empresa
        ).first()

        # Si la relación de comercialización no existe, crea una nueva
        if not comercializa_existente:
            nueva_comercializa = comercializa(
                id_producto=random_producto.id_producto,
                ruc=random_empresa.ruc_empresa
            )
            db.session.add(nueva_comercializa)
    db.session.commit()

    for a in range(15):
        # Selecciona una fecha de entrega aleatoria
        fecha_entrega = fake.date_this_decade()

        # Selecciona un hotel y una empresa de manera aleatoria
        random_hotel = hotel.query.order_by(func.random()).first()
        random_empresa = empresa.query.order_by(func.random()).first()

        # Verifica si la relación de proveeduría ya existe
        provee_existente = provee.query.filter_by(
            id_hotel=random_hotel.id_hotel,
            ruc=random_empresa.ruc_empresa
        ).first()

        # Si la relación de proveeduría no existe, crea una nueva
        if not provee_existente:
            nueva_provee = provee(
                fecha_entrega=fecha_entrega,
                id_hotel=random_hotel.id_hotel,
                ruc=random_empresa.ruc_empresa
            )
            db.session.add(nueva_provee)
    db.session.commit()

    for a in range(15):
        # Selecciona un hotel y un trabajador de manera aleatoria
        random_hotel = hotel.query.order_by(func.random()).first()
        random_personal = personal.query.order_by(func.random()).first()

        # Verificar si la asociación ya existe
        asociacion_existente = trabaja.query.filter_by(
            id_hotel=random_hotel.id_hotel,
            dni_personal=random_personal.dni_personal
        ).first()

        # Si la asociación no existe, crea una nueva
        if not asociacion_existente:
            nueva_asociacion = trabaja(
                id_hotel=random_hotel.id_hotel,
                dni_personal=random_personal.dni_personal
            )
        db.session.add(nueva_asociacion)
    db.session.commit()

    for _ in range(20):
        random_id_habitacion = habitacion.query.order_by(func.random()).first()
        random_dni_cliente = cliente.query.order_by(func.random()).first()
        fecha_reservada = fake.date_between(start_date='today', end_date='+30y')

        # Verificar si ya existe la combinación
        asociacion_existente = reservacion.query.filter_by(
            id_habitacion= random_id_habitacion.id_habitacion,
            dni_cliente= random_dni_cliente.dni_cliente,
            fecha_reservada=fecha_reservada
        ).first()

        if not asociacion_existente:
            # La combinación no existe, se puede crear la reserva
            nueva_asociacion = reservacion(
                id_habitacion= random_id_habitacion.id_habitacion,
                dni_cliente= random_dni_cliente.dni_cliente,
                fecha_reservada=fecha_reservada
            )
        db.session.add(nueva_asociacion)
    db.session.commit()

# Crea las tablas
with app.app_context():
    db.create_all()
    create_fake_data()

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True, port=5000)
