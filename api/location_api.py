from flask import Blueprint

location_bp = Blueprint("location", __name__)


@location_bp.route("/manage")
def location_management():
    return "這是地點管理頁面"
