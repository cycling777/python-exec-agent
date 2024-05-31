import requests

def access_google():
    url = "https://www.google.com"
    response = requests.get(url)
    print("Status Code:", response.status_code)
    print("Headers:", response.headers)
    print("Content:", response.text[:500])  # 最初の500文字のみ表示

access_google()