
from flask import Flask ,jsonify ,request
# del modulo flask importar la clase Flask y los métodos jsonify,request
from flask_cors import CORS       # del modulo flask_cors importar CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app=Flask(__name__)  # crear el objeto app de la clase Flask
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend

# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://alzaidel:Clavedelsql@alzaidel.mysql.pythonanywhere-services.com/alzaidel$proyectoFinal'
# URI de la BBDD                          driver de la BD  user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow

# defino la tabla
class Persona(db.Model):   # la clase Persona hereda de db.Model
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    nombre=db.Column(db.String(100))
    apellido=db.Column(db.String(100))
    edad=db.Column(db.Integer)
    email=db.Column(db.String(100))
    foto=db.Column(db.String(400))
    def __init__(self,nombre,apellido,edad,email,foto):   #crea el  constructor de la clase
        self.nombre=nombre   # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.apellido=apellido
        self.edad=edad
        self.email=email
        self.foto=foto


    #  si hay que crear mas tablas , se hace aqui


with app.app_context():
    db.create_all()  # aqui crea todas las tablas
#  ************************************************************
class PersonaSchema(ma.Schema):
    class Meta:
        fields=('id','nombre','apellido','edad','email','foto')


persona_schema=PersonaSchema()            # El objeto persona_schema es para traer una persona
personas_schema=PersonaSchema(many=True)  # El objeto personas_schema es para traer multiples registros de persona


# crea los endpoint o rutas (json)
@app.route('/personas',methods=['GET'])
def get_Personas():
    all_personas=Persona.query.all()         # el metodo query.all() lo hereda de db.Model
    result=personas_schema.dump(all_personas)  # el metodo dump() lo hereda de ma.schema y
                                                 # trae todos los registros de la tabla
    return jsonify(result)                       # retorna un JSON de todos los registros de la tabla


@app.route('/personas/<id>',methods=['GET'])
def get_persona(id):
    persona=Persona.query.get(id)
    return persona_schema.jsonify(persona)   # retorna el JSON de una persona recibido como parametro


@app.route('/personas/<id>',methods=['DELETE'])
def delete_persona(id):
    persona=Persona.query.get(id)
    db.session.delete(persona)
    db.session.commit()
    return persona_schema.jsonify(persona)   # me devuelve un json con el registro eliminado

@app.route('/personas', methods=['POST']) # crea ruta o endpoint
def create_persona():
    #print(request.json)  # request.json contiene el json que envio el cliente
    nombre=request.json['nombre']
    apellido=request.json['apellido']
    edad=request.json['edad']
    email=request.json['email']
    foto=request.json['foto']
    new_persona=Persona(nombre,apellido,edad,email,foto)
    db.session.add(new_persona)
    db.session.commit()
    return persona_schema.jsonify(new_persona)

@app.route('/personas/<id>' ,methods=['PUT'])
def update_persona(id):
    persona=Persona.query.get(id)

    persona.nombre=request.json['nombre']
    persona.apellido=request.json['apellido']
    persona.edad=request.json['edad']
    persona.email=request.json['email']
    persona.foto=request.json['foto']

    db.session.commit()
    return persona_schema.jsonify(persona)


# # programa principal *******************************
# if __name__=='__main__':
#     app.run(debug=True, port=5000)    # ejecuta el servidor Flask en el puerto 5000
