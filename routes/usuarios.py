from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, JWTManager, create_access_token, get_jwt
from flask_bcrypt import Bcrypt

from config.db import get_db_connection

import os
from dotenv import load_dotenv

#Cargamos las variables de entorno
load_dotenv()

#Crear blueprint
usuarios_bp = Blueprint("usuarios", __name__)

#Inicializamos Bcrypt
bcrypt = Bcrypt()

@usuarios_bp.route('/registrar', methods=['POST'])
def registrar():
    
    #Obtener del body los datos
    data = request
    
    nombre=data.json.get('nombre')
    email=data.json.get('email')
    password=data.json.get('password')
    
    #Validacion
    if not nombre or not email or not password:
        return jsonify({"Error":"Faltan datos"}), 400

    #Obtener el cursor de la bd
    cursor = get_db_connection()

    try:
        #verificamos que el usuario no exista
        cursor.execute("SELECT * FROM usuarios WHERE email =  %s", (email))
        existing_user = cursor.fetchone()
        
        if existing_user:
            return jsonify({"Error": "El usuario ya existe"}), 400
        
        #Hacemos hash al password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        #Insertar el registro del nuevo usuario en la base de datos
        cursor.execute('''INSERT INTO usuarios (nombre, email, password) values(%s,%s,%s)''',
                       nombre, email, hashed_password)
        
        #Guardamos el nuevo registro
        cursor.connection.commit()
    
    except Exception as e:
        return jsonify({"Error":f"Error al registrar al usuario: {str(e)}"}), 500
    
    finally:
        cursor.close()    