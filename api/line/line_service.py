import requests

# ✅ LINE 訊息 API Token（請更換為你的 Token）
LINE_ACCESS_TOKEN = "zri85gOdraY/o/Qo+6c3udfdjfgEVPDFWrN5k2PcroPp+Bor4MUE/y845/5KW4IH5/E3vyUEpsZtiE41yJuNOvl43SMfI1XqLQMKXglSjGGgE4hor2QOP66uaQY9Qcc2g1jJkMnCE/FSgW+eCNvmbQdB04t89/1O/w1cDnyilFU="
LINE_API_URL = "https://api.line.me/v2/bot/message/push"

def send_line_message(line_id, message):
    """
    發送 LINE 訊息給指定的使用者
    
    :param line_id: 使用者的 LINE ID
    :param message: 要發送的訊息內容
    """
    if not line_id:
        print("❌ 發送失敗，LINE ID 不可為空！")
        return False
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
    }
    
    data = {
        "to": line_id,
        "messages": [{"type": "text", "text": message}],
    }

    try:
        response = requests.post(LINE_API_URL, json=data, headers=headers)
        response.raise_for_status()  # ✅ 檢查是否有錯誤回應
        print(f"✅ 訊息已成功發送給 {line_id}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ 發送訊息失敗：{e}")
        return False
