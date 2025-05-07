from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request, JWTManager
from functools import wraps
from services.auth_service import AuthService

def init_jwt(app):
    """初始化JWT
    
    Args:
        app: Flask应用实例
    """
    jwt = JWTManager(app)
    
    @jwt.decode_key_loader
    def get_decode_key_callback(jwt_header, jwt_data):
        """返回用于解码令牌的密钥"""
        key = app.config['JWT_SECRET_KEY']
        print(f"正在解码令牌，使用密钥：{key[:10]}...")
        return key
    
    @jwt.token_in_blocklist_loader
    def check_if_token_blocked(jwt_header, jwt_payload):
        """检查令牌是否已被加入阻止列表
        
        Args:
            jwt_header: JWT头部
            jwt_payload: JWT载荷
            
        Returns:
            bool: 令牌是否被阻止
        """
        jti = jwt_payload["jti"]
        blocked = AuthService.is_token_blacklisted(jti)
        print(f"检查令牌（JTI: {jti}）是否被阻止: {blocked}")
        return blocked
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        """处理令牌过期
        
        Args:
            jwt_header: JWT头部
            jwt_payload: JWT载荷
            
        Returns:
            Response: JSON响应
        """
        print(f"令牌已过期: {jwt_payload.get('sub')}")
        return jsonify({
            "error": "令牌已过期", 
            "code": "token_expired"
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        """处理无效令牌
        
        Args:
            error: 错误信息
            
        Returns:
            Response: JSON响应
        """
        print(f"无效令牌错误: {error}")
        print(f"请求头: {request.headers.get('Authorization', '无Authorization头')}")
        return jsonify({
            "error": "无效的令牌", 
            "code": "invalid_token"
        }), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        """处理缺少令牌
        
        Args:
            error: 错误信息
            
        Returns:
            Response: JSON响应
        """
        print(f"未授权错误: {error}")
        return jsonify({
            "error": "缺少令牌", 
            "code": "missing_token"
        }), 401
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        """处理已撤销的令牌
        
        Args:
            jwt_header: JWT头部
            jwt_payload: JWT载荷
            
        Returns:
            Response: JSON响应
        """
        print(f"令牌已被撤销: {jwt_payload.get('sub')}")
        return jsonify({
            "error": "令牌已被撤销", 
            "code": "revoked_token"
        }), 401
    
    return jwt
    
def admin_required():
    """确保请求来自活跃的管理员
    
    Returns:
        function: 装饰器函数
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            # 可以在这里添加额外的验证逻辑
            return fn(*args, **kwargs)
        return decorator
    return wrapper 