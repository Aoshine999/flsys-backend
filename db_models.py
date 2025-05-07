from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Administrator(db.Model):
    __tablename__ = 'administrators'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)  # 存储哈希后的密码
    email = db.Column(db.String(100), unique=True)
    full_name = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Administrator {self.username}>'
    
    @property
    def serialize(self):
        """返回序列化的管理员信息，不包含密码"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'is_active': self.is_active
        }
        
    def set_password(self, password):
        """设置哈希密码"""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password, password)
        
    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
        
    @classmethod
    def authenticate(cls, username, password):
        admin = cls.get_by_username(username)
        if admin and admin.check_password(password) and admin.is_active:
            return admin
        return None

# class Model(db.Model):
#     __tablename__ = 'models'
    
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     model_id = db.Column(db.String(200), unique=True, nullable=False)
#     description = db.Column(db.Text, nullable=True)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
#     def __repr__(self):
#         return f'<Model {self.name}>'
        
# class TrainingHistory(db.Model):
#     __tablename__ = 'training_history'
    
#     id = db.Column(db.Integer, primary_key=True)
#     model_id = db.Column(db.String(200), db.ForeignKey('models.model_id'), nullable=False)
#     round = db.Column(db.Integer, nullable=False)
#     accuracy = db.Column(db.Float, nullable=True)
#     loss = db.Column(db.Float, nullable=True)
    
#     model = db.relationship('Model', backref=db.backref('history', lazy=True))
    
#     def __repr__(self):
#         return f'<TrainingHistory {self.model_id} Round {self.round}>'
        
def init_app(app):
    """在Flask应用中初始化数据库"""
    # 获取当前文件的绝对路径
    base_dir = os.path.abspath(os.path.dirname(__file__))
    
    # 创建instance目录（如果不存在）
    instance_path = os.path.join(base_dir, 'instance')
    os.makedirs(instance_path, exist_ok=True)
    
    # 使用绝对路径配置数据库
    db_path = os.path.join(instance_path, 'flimgsys.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    print(f"数据库路径: {db_path}")
    
    # 初始化数据库
    db.init_app(app)
    
    # 在应用上下文中创建所有表（如果不存在）
    with app.app_context():
        db.create_all()
        
        # 检查是否需要创建默认管理员
        if Administrator.query.count() == 0:
            admin = Administrator(
                username='admin',
                email='admin@flimgsys.com',
                full_name='系统管理员',
                is_active=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("创建了默认管理员: admin/admin123") 