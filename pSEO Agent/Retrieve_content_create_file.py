import requests
import json
import os

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

        if task_response.status_code == 200:
            task_data = task_response.json()

            # 設定檔案路徑到 pSEO 目錄
            file_path = os.path.join(os.path.dirname(__file__), "content.txt")
            
            # 將結果儲存到 content.txt 檔案中
            with open(file_path, "w", encoding="utf-8") as file:
                file.write("\n\n")
                json.dump(task_data, file, ensure_ascii=False, indent=4)
                    
                print("搜尋結果已儲存到 content.txt 檔案中")
        else:
            print("無法取得 task 資料，請確認 task_id 是否正確")
else:
    print("登入失敗，請檢查登入資訊")
