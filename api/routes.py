from flask import Blueprint

# 建立 Blueprint（主要 API）
routes_bp = Blueprint('routes', __name__)

# ✅ 匯入不同功能的路由
from api.auth.auth_routes import auth_bp
from api.users.user_routes import user_bp
from api.projects.project_routes import project_bp
from api.routes import routes_bp  # ✅ 確保 `routes.py` 存在並正確匯入

# ✅ 註冊 Blueprint
routes_bp.register_blueprint(auth_bp, url_prefix="/auth")
routes_bp.register_blueprint(user_bp, url_prefix="/users")
routes_bp.register_blueprint(project_bp, url_prefix="/projects")
routes_bp.register_blueprint(routes_bp)  # ✅ 註冊 Blueprint
