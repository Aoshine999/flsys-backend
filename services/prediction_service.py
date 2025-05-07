import torch
import base64
from PIL import Image
import io
import os
import sys
from dotenv import load_dotenv

# 添加当前目录到路径中，确保可以导入同级模块
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# 添加项目根目录到路径
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# 针对直接运行和作为包导入的不同情况处理导入
try:
    # 作为包导入时
    from .model_loader import ModelLoader
    from .models import get_transforms, IMG_SIZE
    print("使用相对导入加载模块")
except ImportError:
    # 直接运行时
    import model_loader
    from models import get_transforms, IMG_SIZE
    ModelLoader = model_loader.ModelLoader
    print("使用绝对导入加载模块")

class PredictionService:
    def __init__(self):
        # 加载环境变量
        load_dotenv(override=True)
        
        # 从环境变量获取类别标签
        self.class_labels = os.getenv('CLASS_LABELS').split(',')
        if not self.class_labels:
            raise ValueError("环境变量 CLASS_LABELS 未设置或为空")
            
        print(f"加载了 {len(self.class_labels)} 个类别标签")
        
        # 使用models.py中定义的transforms函数
        self.transform = get_transforms()
        print(f"使用 {IMG_SIZE}x{IMG_SIZE} 图像大小进行预处理")
    
    def predict(self, model_id, image_data):
        """对图像进行预测
        
        Args:
            model_id (str): 模型ID，格式为"模型名称-其他信息"，如"ResNet18-custom-strategy-FedAvg-2025-04-28"
            image_data (str): Base64编码的图像数据
            
        Returns:
            list: 按概率降序排列的预测结果列表，每项包含label和probability
        """
        try:
            # 解码Base64图像 - 兼容纯base64编码和Data URL格式
            if ',' in image_data:
                # Data URL格式 (data:image/png;base64,实际数据)
                image_bytes = base64.b64decode(image_data.split(',')[1])
            else:
                # 纯base64编码
                image_bytes = base64.b64decode(image_data)
                
            image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
            
            # 预处理图像
            image_tensor = self.transform(image).unsqueeze(0)
            
            # 加载模型
            model = ModelLoader.load_model(model_id)
            
            # 执行预测
            with torch.no_grad():
                outputs = model(image_tensor)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)[0]
            
            # 整理预测结果
            predictions = [
                {
                    "label": label,
                    "probability": float(prob)
                }
                for label, prob in zip(self.class_labels, probabilities)
            ]
            
            # 按概率降序排序
            predictions.sort(key=lambda x: x["probability"], reverse=True)
            
            return predictions
            
        except Exception as e:
            print(f"预测过程中发生错误: {str(e)}")
            import traceback
            print(traceback.format_exc())
            raise
    

if __name__ == "__main__":
    try:
        # 设置.env文件路径
        dotenv_path = os.path.join(root_dir, '.env')
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
            print(f"从 {dotenv_path} 加载环境变量")
        else:
            print(f"警告: .env文件不存在于 {dotenv_path}")
        
        # 从本地文件加载图像并转换为base64
        def image_to_base64(image_path):
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
                # 根据文件扩展名确定MIME类型
                ext = os.path.splitext(image_path)[1].lower()
                if ext == '.png':
                    mime = 'image/png'
                elif ext in ['.jpg', '.jpeg']:
                    mime = 'image/jpeg'
                else:
                    mime = 'image/jpeg'  # 默认
                return f"data:{mime};base64,{encoded_string.decode('utf-8')}"
        
        # 图像文件路径 - 现在指向FLSYS-BACKEND同级的test目录
        parent_dir = os.path.dirname(root_dir)  # 获取FLSYS-BACKEND的父目录
        image_path = os.path.join(parent_dir, "test", "test_00011_label_9.png")
        print(f"尝试加载图像: {image_path}")
        
        # 检查文件是否存在
        if not os.path.exists(image_path):
            print(f"错误: 找不到图像文件 {image_path}")
            # 尝试使用绝对路径
            abs_path = os.path.abspath(image_path)
            print(f"尝试绝对路径: {abs_path}")
            if not os.path.exists(abs_path):
                print(f"错误: 找不到图像文件 {abs_path}")
                sys.exit(1)
            else:
                image_path = abs_path
        
        # 转换为base64
        image_data = image_to_base64(image_path)
        print("图像已成功转换为base64格式")
        
        # 初始化预测服务
        prediction_service = PredictionService()
        
        # 指定要使用的模型ID
        model_id = "mobilenet_v3_small-central_model-2025-04-28_19-23-09"  # 修改为您要测试的实际模型ID
        print(f"使用模型: {model_id}")
        
        # 执行预测
        predictions = prediction_service.predict(model_id, image_data)
        
        # 打印预测结果
        print("\n预测结果:")
        for pred in predictions:
            print(f"{pred['label']}: {pred['probability']:.4f}")
    
    except Exception as e:
        import traceback
        print(f"错误: {str(e)}")
        print(traceback.format_exc())

