from flask import Blueprint, request, jsonify, render_template, session
from db import get_db_connection
import api.users.user_service as user_service  # ✅ 確保導入 user_service
import api.line.line_service as line_service  # ✅ 新增 line_service 來發送 LINE 訊息
from api.line.line_service import send_line_message

user_bp = Blueprint("user", __name__)  # ✅ 定義 Blueprint

# 假設某個使用者的 LINE ID
user_line_id = "Uxxxxxxxxxxxxxxxxxxxxxx"  # 這裡放使用者的 LINE ID
message = "您好，這是一則測試訊息！"

# 發送訊息
send_line_message(user_line_id, message)


# ✅ 新增 IT 系統使用者
@user_bp.route("/add", methods=["POST"])
def add_user():
    if "user" not in session or session.get("role") != "admin":  # ✅ 確保只有管理員能新增
        return jsonify({"error": "無權限新增使用者"}), 403

    data = request.json
    username = data.get("username")
    password = data.get("password")
    line_id = data.get("line_id")  # ✅ 改為 `line_id`
    role = data.get("role", "user")  # 預設角色是 user

    if not username or not password or not line_id:
        return jsonify({"error": "請提供帳號、密碼、LINE ID"}), 400

    user = user_service.get_user_by_username(username)
    if user is not None:
        return jsonify({"error": "使用者名稱已存在"}), 400

    success = user_service.create_user(username, password, line_id, role)
    if success:
        # ✅ 發送 LINE 訊息
        line_service.send_line_message(line_id, f"🎉 歡迎 {username} 加入 IT 系統！")

        return jsonify({"message": "IT 使用者新增成功，已發送 LINE 歡迎訊息"}), 201
    else:
        return jsonify({"error": "資料庫錯誤"}), 500


# ✅ 顯示新增使用者的頁面
@user_bp.route("/add_form", methods=["GET"])
def add_user_form():
    return render_template("user_templates/add_user.html")


# ✅ 顯示使用者列表的頁面
@user_bp.route("/list", methods=["GET"])
def list_users_page():
    users = user_service.get_all_users()
    return render_template("user_templates/user_list.html", users=users)
