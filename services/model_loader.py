import os
import sys
import torch
import importlib
from dotenv import load_dotenv

# 加载环境变量
if __name__ == "__main__":
    # 添加项目根目录到Python路径
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    # 确保能找到.env文件
    dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    load_dotenv(dotenv_path)
else:
    load_dotenv(override=True)

class ModelLoader:
    @staticmethod
    def load_model(model_id):
        try:
            # 获取环境变量
            project_dir = os.getenv('FLOWER_PROJECT_DIR')
            
            if not project_dir:
                raise ValueError("环境变量 FLOWER_PROJECT_DIR 未设置")
            
            print(f"Flower项目目录: {project_dir}")
            
            try:
                # 针对直接运行和作为包导入的不同情况处理导入
                try:
                    # 作为包导入时
                    from . import models
                    print("使用相对导入加载models模块")
                except ImportError:
                    # 直接运行时
                    import models
                    print("使用绝对导入加载models模块")
                
                # 获取模型名称部分（例如从"Net-custom-strategy-FedAvg-2025-04-28_17-03-02"提取"Net"）
                model_name = model_id.split('-')[0]  # 获取模型名称部分
                print(f"模型名称: {model_name}")
                
                # 获取类别数量
                num_classes = len(os.getenv('CLASS_LABELS').split(','))
                print(f"类别数量: {num_classes}")
                
                # 使用统一的模型创建接口
                model = models.create_model(model_name, num_classes)
                print(f"使用create_model创建{model_name}模型")
                
                # 加载权重
                weights_dir = os.path.join(
                    project_dir,
                    os.getenv('MODEL_WEIGHTS_SUBDIR'),
                    f"{model_id}/best_model.pth"
                )
                
                print(f"加载权重文件: {weights_dir}")
                if not os.path.exists(weights_dir):
                    raise FileNotFoundError(f"权重文件不存在: {weights_dir}")
                
                model.load_state_dict(torch.load(weights_dir))
                model.eval()
                
                print("模型加载成功")
                return model
            except Exception as e:
                print(f"加载模型时出错: {str(e)}")
                import traceback
                print(traceback.format_exc())
                raise
        finally:
            # 如果有临时添加的路径，移除它
            if 'project_dir' in locals() and project_dir in sys.path:
                sys.path.remove(project_dir) 


