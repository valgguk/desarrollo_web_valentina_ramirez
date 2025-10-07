# app/config.py
class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://cc5002:programacionweb@localhost:3306/tarea2?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "programacionweb2025" 
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8MB global
    # Cambiado a static/uploads para servir directamente via url_for('static', filename='uploads/...')
    UPLOAD_FOLDER = "app/static/uploads"
    ALLOWED_IMAGE_EXTENSIONS = {"png","jpg","jpeg","gif","webp"}