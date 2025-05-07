from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from .auth_handlers import AuthHandler

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """管理员登录API
    
    请求体:
    {
      "username": "用户名",
      "password": "密码"
    }
    
    成功返回:
    {
      "admin": {
        "id": 数字,
        "username": "字符串",
        "email": "字符串",
        "full_name": "字符串",
        "is_active": 布尔值
      },
      "token": "JWT令牌字符串"
    }
    
    失败返回:
    {
      "error": "错误信息",
      "code": "错误代码"
    }
    """
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({
                "error": "用户名和密码不能为空", 
                "code": "missing_credentials"
            }), 400
            
        admin, token = AuthHandler.login(username, password)
        
        if not admin or not token:
            return jsonify({
                "error": "用户名或密码错误", 
                "code": "invalid_credentials"
            }), 401
            
        return jsonify({
            "admin": admin.serialize,
            "token": token
        })
        
    except Exception as e:
        return jsonify({
            "error": f"登录失败: {str(e)}", 
            "code": "system_error"
        }), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """管理员登出API
    
    成功返回:
    {
      "success": true,
      "message": "退出成功"
    }
    
    失败返回:
    {
      "error": "错误信息"
    }
    """
    try:
        success = AuthHandler.logout()
        if success:
            return jsonify({
                "success": True,
                "message": "退出成功"
            })
        else:
            return jsonify({
                "error": "退出失败", 
                "code": "logout_failed"
            }), 500
    except Exception as e:
        return jsonify({
            "error": f"退出失败: {str(e)}", 
            "code": "system_error"
        }), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    """获取当前管理员信息API
    
    成功返回:
    {
      "admin": {
        "id": 数字,
        "username": "字符串",
        "email": "字符串",
        "full_name": "字符串",
        "is_active": 布尔值
      }
    }
    
    失败返回:
    {
      "error": "错误信息",
      "code": "错误代码"
    }
    """
    try:
        admin = AuthHandler.get_current_admin()
        
        if not admin:
            return jsonify({
                "error": "找不到管理员信息", 
                "code": "admin_not_found"
            }), 404
            
        return jsonify({
            "admin": admin.serialize
        })
        
    except Exception as e:
        return jsonify({
            "error": f"获取管理员信息失败: {str(e)}", 
            "code": "system_error"
        }), 500