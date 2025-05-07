"""提供Flower联邦学习模拟训练的进程管理和实时日志流功能"""

import os
import subprocess
from dotenv import load_dotenv

load_dotenv(override=True)

class SimulationRunner:
    """管理Flower联邦学习模拟训练进程的启动和日志流处理"""
    def __init__(self, socketio, client_sid):
        self.socketio = socketio
        self.client_sid = client_sid
        self.project_dir = os.getenv('FLOWER_PROJECT_DIR')
        self.start_script = os.getenv('FLOWER_START_SCRIPT')
    
    def start_simulation(self, config):
        """启动Flower联邦学习模拟训练进程"""
        def stream_output(process):
            """处理进程输出流并发送日志消息"""
            for line in iter(process.stdout.readline, ''):
                self.socketio.emit('simulation_log',
                                 {'message': line.strip()},
                                 room=self.client_sid)
            
            return_code = process.wait()
            if return_code == 0:
                self.socketio.emit('simulation_log',
                                 {'message': '模拟成功完成',
                                  'exit_code': 0},
                                 room=self.client_sid)
            else:
                self.socketio.emit('simulation_error',
                                 {'message': f'模拟失败，退出码 {return_code}',
                                  'exit_code': return_code},
                                 room=self.client_sid)
        
        try:
            # 构建命令
            cmd = ['python', self.start_script]
            for key, value in config.items():
                cmd.extend([f'--{key}', str(value)])
            
            # 启动进程
            process = subprocess.Popen(
                cmd,
                cwd=self.project_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,
                universal_newlines=True
            )
            
            # 在后台任务中处理输出
            self.socketio.start_background_task(stream_output, process)
            
        except Exception as e:
            self.socketio.emit('simulation_error',
                             {'message': str(e),
                              'exit_code': -1},
                             room=self.client_sid) 