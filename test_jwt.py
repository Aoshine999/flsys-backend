import requests
import json
import time

BASE_URL = 'http://localhost:8000/api/auth'

def test_jwt_flow():
    """测试JWT认证流程"""
    # 1. 登录获取令牌
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    print("1. 尝试登录...")
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    print(f"状态码: {response.status_code}")
    
    if response.status_code != 200:
        print("登录失败!")
        print(response.text)
        return
    
    login_result = response.json()
    token = login_result.get('token')
    print("登录成功，获取到令牌!")
    
    # 2. 使用令牌获取用户信息
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    print("\n2. 使用令牌获取用户信息...")
    response = requests.get(f"{BASE_URL}/me", headers=headers)
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        user_info = response.json()
        print("用户信息获取成功:")
        print(json.dumps(user_info, ensure_ascii=False, indent=2))
    else:
        print("获取用户信息失败!")
        print(response.text)
    
    # 3. 使用令牌调用普通API
    print("\n3. 使用令牌调用其他API...")
    response = requests.get("http://localhost:8000/api/models/", headers=headers)
    print(f"状态码: {response.status_code}")
    
    # 4. 登出
    print("\n4. 登出...")
    response = requests.post(f"{BASE_URL}/logout", headers=headers)
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        print("登出成功!")
    else:
        print("登出失败!")
        print(response.text)
    
    # 5. 使用已登出的令牌尝试获取用户信息
    print("\n5. 使用已登出的令牌尝试获取用户信息（应该失败）...")
    response = requests.get(f"{BASE_URL}/me", headers=headers)
    print(f"状态码: {response.status_code}")
    print(response.text)
    
    # 6. 再次登录
    print("\n6. 再次登录获取新令牌...")
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    new_token = response.json().get('token')
    new_headers = {
        "Authorization": f"Bearer {new_token}"
    }
    
    # 7. 使用新令牌获取用户信息
    print("\n7. 使用新令牌获取用户信息...")
    response = requests.get(f"{BASE_URL}/me", headers=new_headers)
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        user_info = response.json()
        print("用户信息获取成功:")
        print(json.dumps(user_info, ensure_ascii=False, indent=2))
    else:
        print("获取用户信息失败!")
        print(response.text)

if __name__ == "__main__":
    test_jwt_flow() 