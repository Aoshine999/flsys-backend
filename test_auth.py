import requests
import json
import sys

BASE_URL = 'http://localhost:8000/api/auth'

def test_login(username, password):
    """测试登录API
    
    Args:
        username (str): 用户名
        password (str): 密码
    """
    url = f"{BASE_URL}/login"
    data = {
        "username": username,
        "password": password
    }
    
    response = requests.post(url, json=data)
    print(f"状态码: {response.status_code}")
    
    try:
        result = response.json()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return result.get('token')
    except:
        print("返回内容不是有效的JSON")
        print(response.text)
        return None

def test_me(token):
    """测试获取当前用户信息API
    
    Args:
        token (str): JWT令牌
    """
    url = f"{BASE_URL}/me"
    # 确保Bearer和token之间有空格
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    print(f"使用的Authorization头: {headers['Authorization']}")
    
    response = requests.get(url, headers=headers)
    print(f"\n状态码: {response.status_code}")
    
    try:
        result = response.json()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except:
        print("返回内容不是有效的JSON")
        print(response.text)

def test_logout(token):
    """测试登出API
    
    Args:
        token (str): JWT令牌
    """
    url = f"{BASE_URL}/logout"
    # 确保Bearer和token之间有空格
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    print(f"使用的Authorization头: {headers['Authorization']}")
    
    response = requests.post(url, headers=headers)
    print(f"\n状态码: {response.status_code}")
    
    try:
        result = response.json()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except:
        print("返回内容不是有效的JSON")
        print(response.text)

if __name__ == "__main__":
    # 默认用户名和密码
    username = "admin"
    password = "admin123"
    
    # 从命令行参数获取用户名和密码（如果提供）
    if len(sys.argv) > 1:
        username = sys.argv[1]
    if len(sys.argv) > 2:
        password = sys.argv[2]
    
    print(f"测试登录 (用户名: {username})")
    token = test_login(username, password)
    
    if token:
        print("\n测试获取用户信息")
        test_me(token)
        
        print("\n测试登出")
        test_logout(token)
        
        print("\n再次测试获取用户信息（应该失败）")
        test_me(token)
    else:
        print("登录失败，无法继续测试") 