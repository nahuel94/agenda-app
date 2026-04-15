from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from db import get_connection
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    # hash de password
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO usuarios (username, password) VALUES (%s, %s)",
            (username, hashed.decode('utf-8'))
        )
        conn.commit()

        return jsonify({"mensaje": "Usuario creado"})
    
    except Exception as e:
        return jsonify({"error": "Usuario ya existe"}), 400

    finally:
        cur.close()
        conn.close()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, password FROM usuarios WHERE username = %s",
        (username,)
    )

    user = cur.fetchone()

    cur.close()
    conn.close()

    if user:
        user_id, hashed_password = user

        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            
            token = create_access_token(identity=str(user_id))

            return jsonify(access_token=token)

    return jsonify({"error": "Credenciales incorrectas"}), 401