import bcrypt
from db import get_db_connection

def hash_password(password):
    """加密密碼"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def check_password(password, hashed_password):
    """驗證密碼"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def get_user_by_username(username):
    """根據帳號查詢使用者"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user


def create_user(username, password, line_id, role):
    """新增使用者"""
    hashed_pw = hash_password(password)

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password, line_id, role) VALUES (%s, %s, %s, %s)",
            (username, hashed_pw, line_id, role),
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"❌ 新增使用者錯誤：{e}")
        return False
    finally:
        cursor.close()
        conn.close()


def get_all_users():
    """取得所有使用者"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, line_id, role, created_at FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users
import requests

LINE_ACCESS_TOKEN = "你的_LINE_ACCESS_TOKEN".strip()  # ✅ 確保沒有多餘空格
LINE_API_URL = "https://api.line.me/v2/bot/message/push"

def send_line_message(line_id, message):
    """發送 LINE 訊息，確保 UTF-8 編碼"""
    headers = {
        "Content-Type": "application/json; charset=UTF-8",  # ✅ 確保 Content-Type 使用 UTF-8
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN.encode('utf-8').decode('utf-8')}",  # ✅ 確保 header 也是 UTF-8
    }

    # ✅ 確保 message 內容是 UTF-8
    message_utf8 = message.encode("utf-8").decode("utf-8")

    data = {
        "to": line_id,
        "messages": [{"type": "text", "text": message_utf8}],
    }

    print("🔍 檢查 line_id:", line_id)
    print("🔍 檢查 message:", message_utf8)
    print("🔍 檢查 headers:", headers)

    try:
        response = requests.post(LINE_API_URL, json=data, headers=headers)

        if response.status_code == 200:
            print(f"✅ 已成功發送訊息給 {line_id}")
        else:
            print(f"❌ 發送訊息失敗 (狀態碼 {response.status_code}): {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ 發送訊息請求失敗: {str(e)}")
