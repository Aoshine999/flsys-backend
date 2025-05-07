## Flask 后端设计文档：Flower 联邦学习模拟与预测平台

**1. 项目概述与目标**

**本项目旨在创建一个 Flask 后端服务，用于支持一个前端界面，该界面用于：**

* **展示和选择**：展示 Flower 联邦学习项目目录下可用于预测的模型权重文件。
* **图像预测**：接收前端上传的图片和选定的模型名称，使用 Flower 项目中相应的模型和权重进行推理，并返回预测结果。
* **训练历史查看 (可选)**：提供接口以获取 Flower 项目目录下存储的训练历史记录文件（如 JSON 格式）。
* **启动 Flower 模拟**：接收前端传递的配置参数，在本地 Flower 项目目录下启动相应的 Flower 训练/模拟进程，并**实时**将该进程的终端输出流式传输回前端。

 **核心特点：** **本后端**不使用数据库**，所有模型相关的文件（权重** **.pth**、模型定义 **.py**、历史记录 **.json** **等）均**统一存储和管理在指定的 Flower Framework 开发的项目目录**下。**

 **2. 技术栈**

* **框架:** **Flask**
* **实时通信:** **Flask-SocketIO (用于日志流)**
* **进程管理:** **Python** **subprocess**
* **图像处理:** **Pillow**
* **模型处理:** **PyTorch (**torch**,** **torchvision**)
* **配置管理:** **python-dotenv** **(推荐，用于** **.env** **文件)**
* **路径/系统交互:** **Python** **os**, **sys**
* **动态导入 (可选):** **Python** **importlib** **或** **sys.path** **修改**
* **跨域处理:** **Flask-Cors**

**3. 配置要求 (通过** **.env** **文件管理)**

**后端启动和运行依赖于以下配置项，建议存储在项目根目录的** **.env** **文件中：**

| **环境变量**                | **描述**                                                                                                                            | **示例值**                          | **必须** |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- | -------------- |
| **FLOWER_PROJECT_DIR**      | **Flower 项目的根目录绝对路径，或相对于 backend-flask 的路径。**                                                                    | **../flower-project**               | **是**   |
| **FLOWER_START_SCRIPT**     | **在** **FLOWER_PROJECT_DIR** **中用于启动 Flower 进程的脚本名称或命令。**                                              | **run_flower.py**                   | **是**   |
| **MODEL_WEIGHTS_SUBDIR**    | **在** **FLOWER_PROJECT_DIR** **内，存放**预测用 **.pth** **文件的子目录名。**                              | **saved_models**                    | **是**   |
| **MODEL_DEFINITION_MODULE** | **在** **FLOWER_PROJECT_DIR** **内，定义模型架构 (**nn.Module**) 的 Python 模块的相对路径（相对于项目根目录）。** | **model** **(对应 model.py)** | **是**   |
| **HISTORY_SUBDIR**          | **(可选) 在** **FLOWER_PROJECT_DIR** **内，存放训练历史** **.json** **文件的子目录名。**                    | **results**                         | **否**   |
| **CLASS_LABELS**            | **预测任务的类别标签列表，以逗号分隔的字符串。**顺序必须与模型输出一致**。**                                                  | **猫,狗,鸟**                        | **是**   |
| **IMG_SIZE**                | **模型期望的输入图像大小 (正方形)。**                                                                                               | **224**                             | **是**   |
| **FLASK_SECRET_KEY**        | **Flask 和 Flask-SocketIO 用于会话安全的密钥。**                                                                                    | **一个随机且安全的字符串**          | **是**   |

**4. 后端项目结构**

```
flsys-backend/
├── app.py                 # Flask 应用主入口和 SocketIO 事件处理器
├── api/                   # 存放 REST API 蓝图和相关逻辑
│   ├── __init__.py        # 将目录标记为 Python 包
│   ├── routes.py          # 定义 /api/* 的 HTTP 路由 (使用 Flask Blueprint)
│   └── handlers.py        # 实现 API 路由的具体处理函数
├── services/              # 存放核心业务逻辑和服务类
│   ├── __init__.py
│   ├── model_loader.py    # 负责动态加载 Flower 项目中的模型架构和权重
│   ├── prediction_service.py # 处理图像预处理和模型推理逻辑
│   ├── file_service.py    # 处理文件系统交互 (查找模型、读取历史文件)
│   └── simulation_runner.py # 负责启动和管理 Flower 子进程
├── utils/                 # (可选) 存放通用辅助函数或类
│   ├── __init__.py
│   └── helpers.py
├── .env                   # 存储环境变量 (非常重要!)
├── requirements.txt       # Python 依赖项
└── wsgi.py                # (可选) WSGI 入口点，用于 Gunicorn 部署

# --- Flower 项目目录 (独立于 backend-flask，但后端依赖其路径和内容) ---
# /path/to/your/flower-project/
# ├── run_flower.py
# ├── model.py
# ├── global_models/
#     ├── (模型)_(时间)
#         ├── best_model.pth
#         ├── result.json     #存储模型每轮的训练准确率，loss值，以及整个模型的训练时间。  
# ├── results/
# └── ...
```

**结构说明:**

* **app.py**:

  * **初始化 Flask 应用 (**Flask(__name__)**)。**
* **初始化 Flask-SocketIO (**SocketIO(app, ...)**).**
* **加载配置 (从** **.env** **文件)。**
* **注册 API 蓝图 (从** **api/routes.py**)。
* **定义** **WebSocket 事件处理器** **(**@socketio.on('connect')**,** **@socketio.on('start_simulation')**, etc.)。这些通常与实时交互紧密相关，放在主文件中比较直观。
* **包含** **if __name__ == '__main__':** **块，用于启动开发服务器 (**socketio.run(app, ...)**).**
* **api/**: 使用 Flask Blueprint 将 REST API 逻辑组织起来。

  * **routes.py**: 定义蓝图实例 (**Blueprint('api', __name__, url_prefix='/api')**)，并使用 **@api.route(...)** **定义具体的 HTTP 端点 (如** **/models/**, **/predict/**, **/models/.../training_history/**)。这些路由函数通常会调用 **handlers.py** **中的实现。**
* **handlers.py**: 包含处理 HTTP 请求的具体逻辑函数。这些函数会调用 **services/** **中的服务来完成实际工作（如查找模型、执行预测、读取文件）。这有助于保持路由定义的简洁性。**
* **services/**: 存放核心业务逻辑，与 Flask 框架本身解耦。

  * **model_loader.py**: 封装**动态导入** **Flower 项目中模型类和加载权重的复杂逻辑。**
* **prediction_service.py**: 封装图像解码、预处理、调用模型进行推理的逻辑。
* **file_service.py**: 封装扫描目录查找 **.pth** **文件、读取** **.json** **历史文件等文件系统操作。**
* **simulation_runner.py**: 封装构建命令、使用 **subprocess.Popen** **启动 Flower 子进程、以及与** **stream_subprocess_output** **(可以在这里实现或由** **app.py** **调用) 相关的逻辑。**
* **utils/** **(可选)**: 存放可以在项目中多处复用的简单函数，例如日志格式化、配置读取辅助函数等。
* **.env**: 存储所有配置变量，**不应**提交到版本控制。
* **requirements.txt**: 列出所有 Python 依赖。
* **wsgi.py** **(可选)**: 用于生产部署。Gunicorn 等 WSGI 服务器会查找这个文件来加载应用实例。通常内容很简单：

```
# wsgi.py
from app import app, socketio

if __name__ == "__main__":
    # 这里的 run 仅用于本地测试 wsgi 文件是否正常工作
    # 生产环境由 Gunicorn 等服务器调用 app 对象
    socketio.run(app)
```

**5. 后端 API 设计**

**后端将提供以下 HTTP REST API 端点和 WebSocket 事件。**

**5.1 HTTP REST API 端点**

* **GET /api/models/**

  * **目的:** **获取可用于预测的模型列表。**
  * **前端接口:** **getModels(): Promise<Model[]>**
  * **后端操作:**

    * **读取** **FLOWER_PROJECT_DIR** **和** **MODEL_WEIGHTS_SUBDIR** **配置。**
    * **构建完整的权重目录路径。**
    * **扫描该目录，查找所有** **.pth** **文件。**
    * **对于每个找到的** **.pth** **文件，提取不带后缀的文件名。**
  * **成功响应 (200 OK):**

    ```
    {
      "models": [
        {
          "id": "模型文件名A", // 通常是 .pth 文件名（无后缀）
          "name": "模型文件名A", // 同 id
          "description": "" // 描述可为空，或将来扩展
        },
        {
          "id": "模型文件名B",
          "name": "模型文件名B",
          "description": ""
        }
        // ...
      ]
    }
    ```
  * **失败响应:**

    * **500 Internal Server Error**: 如果配置错误或无法读取目录。
* **POST /api/predict/**

  * **目的:** **使用指定模型对上传的图片进行预测。**
  * **前端接口:** **postPrediction(modelId, imageData): Promise<Prediction[]>**
  * **请求体 (JSON)**:

    ```
    {
      "model_id": "模型文件名A", // 对应 /api/models/ 返回的 id
      "image_data": "data:image/jpeg;base64,/9j/4AAQSkZJRg..." // Base64 编码的图像数据
    }

    ```
  * **后端操作:**

  1. **接收** **model_id** **和** **image_data**。
  2. **构建** **.pth** **文件的完整路径 (**FLOWER_PROJECT_DIR **+** **MODEL_WEIGHTS_SUBDIR** **+** **model_id** **+** **.pth**)。
  3. **动态加载模型架构:**

     * **将** **FLOWER_PROJECT_DIR** **临时添加到** **sys.path**。
     * **根据** **MODEL_DEFINITION_MODULE** **配置导入包含模型定义的模块。**
     * **约定:** **需要一种机制将** **model_id** **(文件名) 映射到该模块中定义的具体** **nn.Module** **类名（例如，假设类名与** **model_id** **相同，或首字母大写）。**
     * **实例化该模型类。**
     * **从** **sys.path** **移除** **FLOWER_PROJECT_DIR** **(推荐)。**
  4. **加载** **.pth** **文件中的权重 (**state_dict**) 到实例化的模型。**
  5. **设置模型为评估模式 (**model.eval()**)。**
  6. **解码 Base64 图像数据。**
  7. **使用 Pillow 打开图像，转换为 RGB。**
  8. **应用配置的预处理步骤 (**preprocess**: resize, ToTensor, normalize)。**
  9. **将处理后的图像张量移动到合适的设备 (GPU or CPU)。**
  10. **执行模型推理 (**with torch.no_grad(): ...**)。**
  11. **对模型输出应用 Softmax 得到概率。**
  12. **将概率与配置的** **CLASS_LABELS** **列表结合。**

  * **成功响应 (200 OK):**

    ```
    {
      "predictions": [
        { "label": "猫", "probability": 0.9501 },
        { "label": "狗", "probability": 0.0455 },
        { "label": "鸟", "probability": 0.0044 }
        // ... 按概率降序排列 (可选)
      ]
    }
    ```
  * **失败响应:**

    * **400 Bad Request**: 请求体格式错误、缺少参数、图片解码/处理失败、模型导入/加载失败。
    * **404 Not Found**: 指定的 **model_id** **对应的** **.pth** **文件不存在。**
    * **500 Internal Server Error**: 模型输出维度与 **CLASS_LABELS** **数量不匹配、推理过程中发生意外错误。**
* **GET /api/models/{model_id}/training_history/**

  * **目的:** **(可选) 获取指定模型训练过程的历史记录。**
  * **前端接口:** **getTrainingHistory(modelId): Promise `<TrainingHistoryData>`**
  * **URL 参数:** **{model_id}** **- 模型的 ID (通常是** **.pth** **文件名，假设历史文件名与模型名相关联)。**
  * **后端操作:**

    1. **检查** **HISTORY_SUBDIR** **是否已配置。**
    2. **构建历史文件 (**.json**) 的完整路径 (**FLOWER_PROJECT_DIR **+** **HISTORY_SUBDIR** **+** **model_id** **+** **.json**)。**注意:** **这里的** **model_id** **与历史文件名的关联需要明确约定。**
    3. **读取并解析 JSON 文件。**
    4. **(可选) 验证 JSON 文件是否包含** **rounds**, **accuracies**, **losses** **键。**
  * **检查** **HISTORY_SUBDIR** **是否已配置。**
  * **构建历史文件 (**.json**) 的完整路径 (**FLOWER_PROJECT_DIR **+** **HISTORY_SUBDIR** **+** **model_id** **+** **.json**)。**注意:** **这里的** **model_id** **与历史文件名的关联需要明确约定。**
  * **读取并解析 JSON 文件。**
  * **(可选) 验证 JSON 文件是否包含** **rounds**, **accuracies**, **losses** **键。**
  * **成功响应 (200 OK):**

    {
    "rounds": [1, 2, 3, ...],
    "accuracies": [0.65, 0.72, 0.78, ...],
    "losses": [0.88, 0.65, 0.52, ...],
    "total_training_time": "2 hours 30 minutes" // 可选字段
    }
  * **失败响应:**

    * **404 Not Found**: 历史文件未找到。
    * **500 Internal Server Error**: 读取或解析 JSON 文件失败，或格式无效。
    * **501 Not Implemented**: 如果 **HISTORY_SUBDIR** **未配置。**

**5.2 WebSocket API (用于启动模拟和日志流)**

**使用 Flask-SocketIO 实现实时双向通信。**

* **连接事件:**

  * **connect**: 客户端成功连接时触发。后端可以记录连接 (**request.sid**)。
  * **disconnect**: 客户端断开连接时触发。后端可以进行清理（如果需要）。
* **客户端 -> 服务器 事件:**

  * **start_simulation**
    * **目的:** **请求后端启动 Flower 模拟进程。**
    * **发送数据 (JSON):** **前端发送一个包含配置参数的对象。这些参数将被传递给** **FLOWER_START_SCRIPT**。

      ```
      {
        "rounds": 10,
        "min_clients": 2,
        "fraction_fit": 0.8,
        "learning_rate": 0.01
        // ... 其他 Flower 脚本需要的参数
      }
      ```
    * **后端操作:**

      1. **接收配置数据。**
      2. **验证** **FLOWER_PROJECT_DIR** **和** **FLOWER_START_SCRIPT** **配置。**
      3. **构建命令行：将** **FLOWER_START_SCRIPT** **和接收到的配置参数组合成一个列表 (e.g.,** **['python', 'run_flower.py', '--rounds', '10', ...]**)。
      4. **使用** **subprocess.Popen** **启动子进程：**

         * **设置** **cwd=FLOWER_PROJECT_PATH** **确保在 Flower 项目目录下执行。**
         * **捕获** **stdout** **和** **stderr** **(合并到一个流)。**
         * **使用行缓冲 (**bufsize=1**) 和文本模式 (**text=True**)。**
      5. **设置** **cwd=FLOWER_PROJECT_PATH** **确保在 Flower 项目目录下执行。**
      6. **捕获** **stdout** **和** **stderr** **(合并到一个流)。**
      7. **使用行缓冲 (**bufsize=1**) 和文本模式 (**text=True**)。**
      8. **启动一个后台线程 (**socketio.start_background_task**) 来执行** **stream_subprocess_output** **函数。**
      9. **向**发起请求的客户端**发送一个确认消息 (可选)。**
* **服务器 -> 客户端 事件:**

  * **simulation_log**

    * **目的:** **将 Flower 进程的标准输出/错误实时发送给前端。**
    * **发送数据 (JSON)**:

      ```
      {
        "message": "模拟成功完成。",
        "exit_code": 0
      }
      ```
    * **触发时机:****当****stream_subprocess_output** **检测到子进程正常退出 (**return_code == 0**) 时。**
  * simulation_error

    * **目的:** **通知前端 Flower 进程异常结束或启动/流式传输过程中发生错误。**
    * **发送数据 (JSON)**:

      ```
      {
        "message": "模拟失败，退出码 1。", // 或其他错误信息
        "exit_code": 1 // 或其他非零退出码，或 -1 表示后端错误
      }
      ```
    * **触发时机:** **当子进程异常退出 (**return_code != 0**) 或在启动/流式传输过程中捕获到异常时。**

**6. 关键实现细节**

* **动态模型加载:**

  * **/api/predict** **接口的核心挑战在于动态加载 Flower 项目中的模型定义。**
  * **必须通过修改** **sys.path** **或使用** **importlib** **来访问** **FLOWER_PROJECT_DIR** **下的** **.py** **文件。**
  * **需要明确约定如何根据 API 传入的** **model_id** **(文件名) 找到对应的 Python 类名。最简单的方式是约定两者同名（忽略大小写或特定转换）。**
  * **动态导入后，记得恢复** **sys.path** **以避免潜在的命名冲突。**
* **子进程管理:**

  * **使用** **subprocess.Popen** **启动 Flower 进程，并正确设置** **cwd**。
  * **确保捕获** **stdout** **和** **stderr**，最好合并到一个流 (**stderr=subprocess.STDOUT**) 以简化处理。
  * **使用行缓冲 (**bufsize=1**) 和文本模式 (**text=True**) 以便实时读取和发送日志。**
* **实时日志流:**

  * **socketio.start_background_task** **对于在 Flask-SocketIO 中安全地运行后台任务至关重要。**
  * **使用** **iter(process.stdout.readline, '')** **循环读取子进程输出，这是处理流式输出的标准方式。**
  * **关键:** **使用** **room=request.sid** **(在事件处理器中获取) 或将** **sid** **传递给后台任务，确保日志只发送给发起请求的那个客户端。**
* **错误处理:**

  * **对文件操作 (读取目录、文件)、JSON 解析、图像处理、模型加载、子进程执行等步骤添加健壮的** **try...except** **块。**
  * **使用** **app.logger** **记录详细错误信息。**
  * **向客户端返回清晰的错误信息和合适的 HTTP 状态码或 WebSocket 错误事件。**
* **配置验证:** **在应用启动时检查关键配置（如** **FLOWER_PROJECT_DIR**）是否存在且有效。
* **安全性:**

  * **配置 CORS 策略，生产环境应限制来源。**
  * **虽然此应用不直接处理用户上传文件的存储，但在处理来自 URL 的文件名 (**/api/training_history/**) 时，应进行基本的清理，防止路径遍历攻击。**

**7. 部署注意事项**

* **生产环境应使用 Gunicorn + Eventlet 或 Gevent 来运行 Flask-SocketIO 应用，以支持大量并发 WebSocket 连接。**
* **确保** **.env** **文件中的配置在生产环境中正确设置。**
* **管理好 Flower 进程：如果后端服务重启，正在运行的 Flower 进程可能会变成孤儿进程。需要考虑进程管理策略（虽然对于临时模拟可能问题不大）。**
