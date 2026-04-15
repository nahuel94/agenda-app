from flask import Flask
from routes.tareas import tareas_bp
from routes.auth import auth_bp   # 👈 IMPORTANTE

app = Flask(__name__)

# JWT config (si ya lo tenés)
from flask_jwt_extended import JWTManager
import os

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

# registrar blueprints
app.register_blueprint(tareas_bp)
app.register_blueprint(auth_bp)   # 👈 ESTO FALTA SEGURO

if __name__ == '__main__':
    app.run(debug=True)