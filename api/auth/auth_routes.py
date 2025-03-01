from flask import Blueprint, render_template, request, redirect, url_for, session, make_response
from datetime import timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = request.form.get('remember')  # ✅ 取得「記住我」選項

        print(f"記住我選項：{remember}")  # ✅ Debug 訊息，檢查前端是否有傳入 `remember` 

        if username == "admin" and password == "1234":
            session['user'] = username  
            response = make_response(redirect(url_for("home")))

            if remember:  
                response.set_cookie('remember_me', username, max_age=30*24*60*60)  # ✅ 30天有效
                print("✅ 已設定記住我 Cookie")
            else:
                response.delete_cookie('remember_me')
                print("❌ 未勾選記住我，刪除 Cookie")

            return response

        else:
            return render_template('login.html', error="帳號或密碼錯誤")  

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    """登出並導向登入頁面"""
    session.pop('user', None)  # ✅ 清除 session
    response = make_response(redirect(url_for('auth.login')))  
    response.delete_cookie('remember_me')  # ✅ 刪除「記住我」 Cookie
    print("🔴 已登出，Session 與 Cookie 已清除")  # ✅ Debug 訊息
    return response  

