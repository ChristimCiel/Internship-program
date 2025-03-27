import requests
import json

# 定義 Swagger API 的 base URL 和登入的 endpoint
base_url = "xxxxxxx"
login_url = f"{base_url}login"  # 根據實際的 login endpoint 修改

# 登入資訊
username = "xxxxxx"
password = "xxxxxx"

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
    headers = {
        "Authorization": f"Bearer {token}",
        "accept": "application/json",
        "Content-Type": "application/json"  # 加入 Content-Type header
    }
    # 詢問task id並進行搜尋
    task_id = input("請輸入Task ID：")
    if task_id:
        print("取得的 task_id:", task_id)

        # 使用 task_id 進行下一個查詢
        task_url = f"{base_url}tasks?task_id={task_id}"
        task_response = requests.get(task_url, headers=headers)

        task_data = task_response.json()
        print(task_data)
