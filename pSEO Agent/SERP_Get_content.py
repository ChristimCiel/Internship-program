import requests
import json

# 定義 Swagger API 的 base URL 和登入的 endpoint
base_url = "xxxxx"
login_url = f"{base_url}xxxxx"  # 根據實際的 login endpoint 修改

# 登入資訊
username = "xxxxx"
password = "xxxxx"

# 發送登入請求
login_payload = {
    "username": username,
    "password": password
}

response = requests.post(login_url, json=login_payload)

# 檢查請求是否成功
if response.status_code == 200:
    json_data = response.json()
    token = json_data if isinstance(json_data, str) else json_data.get("token")
    print("取得的 Token:", token)

    # 詢問用戶關鍵字並進行搜尋
    keyword = input("請輸入您想要搜尋的關鍵字：")
    search_url = f"{base_url}search?keyword={keyword}"
    headers = {
        "Authorization": f"Bearer {token}",
        "accept": "application/json",
        "Content-Type": "application/json"  # 加入 Content-Type header
    }

    search_response = requests.get(search_url, headers=headers)
    print(search_response.json())
