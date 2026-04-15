from flask import Blueprint, request, jsonify
from db import get_connection
from flask_jwt_extended import jwt_required, get_jwt_identity

tareas_bp = Blueprint('tareas', __name__)

@tareas_bp.route('/tareas', methods=['POST'])
@jwt_required()
def crear_tarea():
    data = request.get_json()
    descripcion = data.get('descripcion')

    user_id = int(get_jwt_identity())

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO tareas (descripcion, usuario_id) VALUES (%s, %s)",
        (descripcion, user_id)
    )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"mensaje": "Tarea creada"})

@tareas_bp.route('/tareas', methods=['GET'])
@jwt_required()
def obtener_tareas():
    user_id = int(get_jwt_identity())

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, descripcion FROM tareas WHERE usuario_id = %s",
        (user_id,)
    )

    tareas = cur.fetchall()

    cur.close()
    conn.close()

    resultado = []
    for t in tareas:
        resultado.append({
            "id": t[0],
            "descripcion": t[1]
        })

    return jsonify(resultado)

@tareas_bp.route('/tareas/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_tarea(id):
    user_id = get_jwt_identity()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM tareas WHERE id = %s AND usuario_id = %s",
        (id, user_id)
    )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"mensaje": "Tarea eliminada"})

