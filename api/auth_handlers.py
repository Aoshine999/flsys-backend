from services.auth_service import AuthService
from flask_jwt_extended import get_jwt, get_jwt_identity

class AuthHandler:
    @staticmethod
    def login(username, password):
        """管理员登录
        
        Args:
            username (str): 用户名
            password (str): 密码
            
        Returns:
            tuple: (admin, token) 如果成功，否则 (None, None)
        """
        return AuthService.login(username, password)
    
    @staticmethod
    def logout():
        """管理员登出
        
        Returns:
            bool: 是否成功
        """
        jti = get_jwt().get('jti')
        return AuthService.logout(jti)
    
    @staticmethod
    def get_current_admin():
        """获取当前登录的管理员
        
        Returns:
            Administrator: 管理员对象，如果不存在则为None
        """
        # 从JWT获取identity（现在是字符串格式的管理员ID）
        identity = get_jwt_identity()
        # 调用AuthService转换并获取管理员
        return AuthService.get_current_admin(identity) 