import os
import json
from dotenv import load_dotenv

load_dotenv(override=True)

class FileService:
    @staticmethod
    def get_available_models():
        project_dir = os.getenv('FLOWER_PROJECT_DIR')
        models_dir = os.path.join(project_dir, os.getenv('MODEL_WEIGHTS_SUBDIR'))
        
        models = []
        for model_dir in os.listdir(models_dir):
            if os.path.isdir(os.path.join(models_dir, model_dir)):
                models.append({
                    "id": model_dir,
                    "name": model_dir,
                    "description": ""
                })
        
        return models
    
    @staticmethod
    def get_training_history(model_id):
        project_dir = os.getenv('FLOWER_PROJECT_DIR')
        if not project_dir:
            raise ValueError("环境变量 FLOWER_PROJECT_DIR 未设置")
            
        # 调试信息
        # print(f"原始 FLOWER_PROJECT_DIR: {project_dir}")
        
        # 获取正确的项目根目录
        # 如果是相对路径，需要基于当前文件位置正确解析
        if not os.path.isabs(project_dir):
            # 获取当前文件的目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # 向上两级到项目根目录（假设services文件夹在项目根目录下）
            base_dir = os.path.dirname(os.path.dirname(current_dir))
            # 从项目根目录出发解析FLSYS目录
            project_dir = os.path.normpath(os.path.join(base_dir, "FLSYS"))
            
        # 检查是否为正确目录
        # print(f"解析后的项目目录: {project_dir}")
        
        # 确保以下环境变量正确设置，或使用硬编码值
        history_subdir = os.getenv('HISTORY_SUBDIR', 'global_model_param')
        
        history_dir = os.path.join(project_dir, history_subdir)
        history_file = os.path.join(history_dir, model_id, "result.json")
        
        # print(f"最终历史文件路径: {history_file}")
        
        # 检查文件是否存在
        if not os.path.exists(history_file):
            raise FileNotFoundError(f"训练历史文件未找到: {history_file}")
            
        with open(history_file, 'r') as f:
            history = json.load(f)
        
        return history
    
    @staticmethod
    def get_models_with_training_logs():
        """获取具有训练日志的模型列表"""
        project_dir = os.getenv('FLOWER_PROJECT_DIR')
        if not project_dir:
            raise ValueError("环境变量 FLOWER_PROJECT_DIR 未设置")
            
        # 如果是相对路径，需要基于当前文件位置正确解析
        if not os.path.isabs(project_dir):
            # 获取当前文件的目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # 向上两级到项目根目录
            base_dir = os.path.dirname(os.path.dirname(current_dir))
            # 从项目根目录出发解析FLSYS目录
            project_dir = os.path.normpath(os.path.join(base_dir, "FLSYS"))
            
        # 获取日志目录
        log_view_subdir = os.getenv('LOG_VIEW_SUBDIR','wandb')
        log_dir = os.path.join(project_dir, log_view_subdir)

        print(log_dir)
        
        # 检查目录是否存在
        if not os.path.exists(log_dir):
            return []
            
        # 获取所有含有output.log文件的子目录
        models_with_logs = []
        for model_dir in os.listdir(log_dir):
            log_file_path = os.path.join(log_dir, model_dir, "files","output.log")
            if os.path.exists(log_file_path) and os.path.isfile(log_file_path):
                models_with_logs.append({
                    "id": model_dir,
                    "name": model_dir,
                    "description": log_file_path
                })
                
        return models_with_logs
        
    @staticmethod
    def get_model_training_log(model_id):
        """获取指定模型的训练日志内容"""
        project_dir = os.getenv('FLOWER_PROJECT_DIR')
        if not project_dir:
            raise ValueError("环境变量 FLOWER_PROJECT_DIR 未设置")
            
        # 如果是相对路径，需要基于当前文件位置正确解析
        if not os.path.isabs(project_dir):
            # 获取当前文件的目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # 向上两级到项目根目录
            base_dir = os.path.dirname(os.path.dirname(current_dir))
            # 从项目根目录出发解析FLSYS目录
            project_dir = os.path.normpath(os.path.join(base_dir, "FLSYS"))
            
        # 获取日志目录
        log_view_subdir = os.getenv('LOG_VIEW_SUBDIR', 'wandb')
        log_file_path = os.path.join(project_dir, log_view_subdir, model_id, "files","output.log")
        
        # 检查文件是否存在
        if not os.path.exists(log_file_path):
            raise FileNotFoundError(f"训练日志文件未找到: {log_file_path}")
            
        # 读取日志文件内容
        with open(log_file_path, 'r', encoding='utf-8') as f:
            log_content = f.read()
            
        return log_content

if __name__ == "__main__":
    """获取具有训练日志的模型列表"""
    project_dir = os.getenv('FLOWER_PROJECT_DIR')
    if not project_dir:
        raise ValueError("环境变量 FLOWER_PROJECT_DIR 未设置")
        
    # 如果是相对路径，需要基于当前文件位置正确解析
    if not os.path.isabs(project_dir):
        # 获取当前文件的目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 向上两级到项目根目录
        base_dir = os.path.dirname(os.path.dirname(current_dir))
        # 从项目根目录出发解析FLSYS目录
        project_dir = os.path.normpath(os.path.join(base_dir, "FLSYS"))
        
    # 获取日志目录
    log_view_subdir = os.getenv('LOG_VIEW_SUBDIR')
    log_dir = os.path.join(project_dir, log_view_subdir)
    print(log_dir)
    
        
    # 获取所有含有output.log文件的子目录
    models_with_logs = []
    for model_dir in os.listdir(log_dir):
        log_file_path = os.path.join(log_dir, model_dir, "files","output.log")
        if os.path.exists(log_file_path) and os.path.isfile(log_file_path):
            models_with_logs.append({
                "id": model_dir,
                "name": model_dir,
                "log_path": log_file_path
            })
    
    print(models_with_logs)


