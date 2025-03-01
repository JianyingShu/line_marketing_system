import os
import webbrowser
import requests  # 確保有 import requests
from threading import Timer
from flask import Flask, render_template, request, session, redirect, url_for

# ✅ 匯入不同功能的 Blueprint
from api.auth.auth_routes import auth_bp
from api.users.user_routes import user_bp


app = Flask(__name__, template_folder="templates", static_folder="static")

# ✅ 設定 Secret Key（用於 Session）
app.secret_key = "supersecretkey"  # 這裡可以改用環境變數管理

## ✅ 註冊 Blueprint
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(user_bp, url_prefix="/users")


# ✅ LINE 訊息 API 設定
LINE_ACCESS_TOKEN = "你的_LINE_ACCESS_TOKEN"
LINE_API_URL = "https://api.line.me/v2/bot/message/push"

# ✅ 設定首頁，檢查是否登入
@app.route("/")
def home():
    if "user" in session:
        return render_template("index.html")  # ✅ 已登入，顯示首頁
    
    # ✅ 如果 Cookie `remember_me` 存在，自動登入
    username = request.cookies.get('remember_me')
    if username:
        session['user'] = username
        print(f"✅ 自動登入用戶：{username}")
        return render_template("index.html")

    return redirect(url_for("auth.login"))  # ✅ 未登入，跳轉登入頁

@app.route('/test')
def test_page():
    return render_template('test.html')

def send_line_message(line_id, message):
    """發送 LINE 訊息"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN.strip()}",  # 確保沒有多餘空格
    }
    data = {
        "to": line_id,
        "messages": [{"type": "text", "text": message}],
    }

    # 🔍 Debug 訊息
    print("🔍 檢查 line_id:", line_id)
    print("🔍 檢查 message:", message)
    print("🔍 檢查 headers:", headers)

    try:
        response = requests.post(LINE_API_URL, json=data, headers=headers)

        if response.status_code == 200:
            print(f"✅ 已成功發送訊息給 {line_id}")
        else:
            print(f"❌ 發送訊息失敗 (狀態碼 {response.status_code}): {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ 發送訊息請求失敗: {str(e)}")


# ✅ 啟動 Flask 伺服器
if __name__ == "__main__":
    print("✅ 啟動 Flask 伺服器，稍後將自動開啟網頁...")
    app.run(host="0.0.0.0", port=9090, debug=True)
