from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt
from datetime import timedelta, datetime
from db_models import Administrator, db
import re

# 存储已注销的令牌
# 使用字典存储，以支持过期时间检查
blacklisted_tokens = {}

class AuthService:
    @staticmethod
    def login(username, password):
        """验证用户并生成令牌
        
        Args:
            username (str): 用户名
            password (str): 密码
            
        Returns:
            tuple: (admin, token) 如果成功，否则 (None, None)
        """
        admin = Administrator.authenticate(username, password)
        if not admin:
            return None, None
            
        # 生成JWT令牌，有效期1天
        # 将admin.id转换为字符串，因为Flask-JWT-Extended要求subject必须是字符串
        token = create_access_token(
            identity=str(admin.id),  # 转换为字符串
            expires_delta=timedelta(days=1),
            additional_claims={'username': admin.username}
        )
        
        return admin, token
    
    @staticmethod
    def register(username, password, email=None, full_name=None):
        """注册新管理员
        
        Args:
            username (str): 用户名
            password (str): 密码
            email (str, optional): 电子邮件
            full_name (str, optional): 姓名
            
        Returns:
            tuple: (admin, token, errors) 成功时返回(admin, token, None)，失败时返回(None, None, errors)
        """
        errors = {}
        
        # 验证用户名
        if not username or not 3 <= len(username) <= 20:
            errors['username'] = ["用户名长度必须在3-20个字符之间"]
        elif not re.match(r'^[a-zA-Z0-9_]+$', username):
            errors['username'] = ["用户名只允许字母、数字和下划线"]
        elif Administrator.query.filter_by(username=username).first():
            errors['username'] = ["用户名已被使用，请更换其他用户名"]
            
        # 验证密码
        if not password or len(password) < 6:
            errors['password'] = ["密码长度不能小于6位"]
            
        # 验证邮箱（如果提供）
        if email:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                errors['email'] = ["邮箱格式不正确"]
                
        # 如果有错误，返回错误信息
        if errors:
            return None, None, errors
            
        # 创建新管理员
        new_admin = Administrator(
            username=username,
            email=email,
            full_name=full_name,
            is_active=True
        )
        new_admin.set_password(password)
        
        # 保存到数据库
        try:
            db.session.add(new_admin)
            db.session.commit()
            
            # 生成JWT令牌
            token = create_access_token(
                identity=str(new_admin.id),
                expires_delta=timedelta(days=1),
                additional_claims={'username': new_admin.username}
            )
            
            return new_admin, token, None
        except Exception as e:
            db.session.rollback()
            return None, None, {"system": [f"注册失败：{str(e)}"]}
    
    @staticmethod
    def logout(jti):
        """将令牌加入黑名单
        
        Args:
            jti (str): JWT ID
            
        Returns:
            bool: 是否成功
        """
        # 将令牌加入黑名单，过期时间设为24小时
        expiry = datetime.now() + timedelta(days=1)
        blacklisted_tokens[jti] = expiry
        
        # 清理过期的令牌
        AuthService._cleanup_blacklist()
        
        return True
    
    @staticmethod
    def _cleanup_blacklist():
        """清理过期的黑名单令牌"""
        now = datetime.now()
        expired_jtis = [jti for jti, expiry in blacklisted_tokens.items() if expiry < now]
        for jti in expired_jtis:
            blacklisted_tokens.pop(jti, None)
    
    @staticmethod
    def is_token_blacklisted(jti):
        """检查令牌是否在黑名单中
        
        Args:
            jti (str): JWT ID
            
        Returns:
            bool: 是否在黑名单中
        """
        # 检查令牌是否在黑名单中并且未过期
        if jti in blacklisted_tokens:
            if blacklisted_tokens[jti] > datetime.now():
                return True
            else:
                # 令牌已过期，从黑名单中移除
                blacklisted_tokens.pop(jti, None)
        return False
    
    @staticmethod
    def get_current_admin(identity):
        """根据JWT身份获取当前管理员
        
        Args:
            identity: JWT中的身份标识（管理员ID）
            
        Returns:
            Administrator: 管理员对象，如果不存在则为None
        """
        # 因为identity在JWT中是字符串，所以需要转换回整数
        try:
            admin_id = int(identity)
            return Administrator.query.get(admin_id)
        except (ValueError, TypeError):
            return None 