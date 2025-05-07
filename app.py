import os
from flask import Flask, request
from flask_socketio import SocketIO
from flask_cors import CORS
from dotenv import load_dotenv

from api.routes import api_bp
from api.auth_routes import auth_bp
from services.simulation_runner import SimulationRunner
# 导入数据库模型
from db_models import init_app as init_db
from utils.auth_middleware import init_jwt

# 加载环境变量
load_dotenv(override=True)

# 创建Flask应用
app = Flask(__name__)
# 设置固定的密钥，不再依赖环境变量
app.config['SECRET_KEY'] = 'b9842937f99a4ef29f6d3319b7586f15a12f98cba98f70bf56cb29cc2d9450c7'

# 配置JWT
app.config['JWT_SECRET_KEY'] = 'b9842937f99a4ef29f6d3319b7586f15a12f98cba98f70bf56cb29cc2d9450c7'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 24 * 60 * 60  # 24小时
# 更新JWT配置，修改为blocklist
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'

# 配置CORS
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# 初始化数据库
init_db(app)

# 初始化JWT
init_jwt(app)

# 初始化SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# 注册蓝图
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api/auth')

# WebSocket事件处理
@socketio.on('connect')
def handle_connect():
    """处理WebSocket客户端连接事件"""
    print(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    """处理WebSocket客户端断开连接事件"""
    print(f"Client disconnected: {request.sid}")

@socketio.on('start_simulation')
def handle_start_simulation(data):
    """启动Flower模拟训练进程并处理日志流"""
    runner = SimulationRunner(socketio, request.sid)
    runner.start_simulation(data)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='127.0.0.1', port=8000) 