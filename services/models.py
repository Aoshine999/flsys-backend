import torch
import torch.nn as nn
import torch.nn.functional as F
import os
from torchvision import transforms
from torchvision.models import resnet18, mobilenet_v3_small


# 配置常量
IMG_SIZE = int(os.getenv('IMG_SIZE'))
NORMALIZE_MEAN = [0.485, 0.456, 0.406]
NORMALIZE_STD = [0.229, 0.224, 0.225]

# 模型注册表 - 用于将模型ID映射到相应的创建函数
MODEL_REGISTRY = {}

def register_model(model_name):
    """模型注册装饰器，用于将模型创建函数添加到注册表"""
    def decorator(func):
        MODEL_REGISTRY[model_name.lower()] = func
        return func
    return decorator

class Net(nn.Module):
    """Model (simple CNN adapted from 'PyTorch: A 60 Minute Blitz')"""

    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)

@register_model("mobilenet_v3_small")
def get_mobilenet_v3_small_model(num_classes: int):
    """Get MobileNetV3 Small model."""
    model = mobilenet_v3_small()
    
    model.features[0][0] = nn.Conv2d(
        in_channels=3,
        out_channels=16,
        kernel_size=3,
        stride=1,
        padding=1,
        bias=False
    )

    model.classifier[-1] = nn.Linear(
        in_features=1024,
        out_features=num_classes,
    )

    return model

@register_model("resnet18")
def get_resnet18_model(num_classes: int):
    """Get ResNet18 model modified for 32x32 images."""
    # 使用GroupNorm替代BatchNorm
    model = resnet18(
        norm_layer=lambda x: nn.GroupNorm(2, x), num_classes=num_classes
    )
    
    # 修改第一个卷积层，适应32x32输入
    model.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1, bias=False)
    
    # 移除maxpool层，避免过早降低特征图分辨率
    # model.maxpool = nn.Identity()

    # FC层已在初始化时配置为正确的类别数
    return model    

@register_model("net")
def get_net_model(num_classes: int):
    """获取简单CNN模型"""
    model = Net()
    # 这里假设Net的输出层是fc3，我们需要调整它的输出类别
    model.fc3 = nn.Linear(84, num_classes)
    return model

def get_transforms():
    """获取标准的数据预处理转换"""
    return transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=NORMALIZE_MEAN, std=NORMALIZE_STD)
    ])

def create_model(model_name, num_classes):
    """统一的模型创建接口
    
    Args:
        model_name (str): 模型名称，如'resnet18', 'net', 'mobilenet_v3_small'
        num_classes (int): 分类数量
    
    Returns:
        nn.Module: 创建的模型
        
    Raises:
        ValueError: 如果模型名称不在注册表中
    """
    model_name = model_name.lower()
    if model_name in MODEL_REGISTRY:
        return MODEL_REGISTRY[model_name](num_classes)
    else:
        available_models = ', '.join(MODEL_REGISTRY.keys())
        raise ValueError(f"未知模型名称: {model_name}。可用模型: {available_models}")




