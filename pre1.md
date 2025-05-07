## 联邦学习图像识别效果评估平台 - 前后端设计 (Vite + Vue 3 + TS + Element Plus + ECharts / Python + Django)

**核心目标:** **加载并评估****预先训练好**的联邦学习模型在图像识别任务上的效果，包括单张图片预测和训练过程指标（准确率、损失）的可视化展示。本系统不包含联邦学习训练过程本身。

### 第一部分：前端设计 (Vite + Vue 3 + TypeScript + Element Plus + ECharts)

**1. 技术栈:**

* **构建工具:** **Vite**
* **框架:** **Vue 3 (Composition API)**
* **语言:** **TypeScript**
* **UI 库:** **Element Plus (提供预制组件，简化开发)**
* **图表库:** **ECharts (通过** **vue-echarts** **或类似库集成)**
* **HTTP 请求:** **Axios**
* **状态管理:** **Pinia**
* **路由:** **Vue Router**

**2. 项目初始化 (使用 Vite):**

```
# 使用 npm
npm create vite@latest frontend --template vue-ts
# 或使用 yarn
# yarn create vite frontend --template vue-ts

cd frontend
npm install
npm install element-plus axios pinia vue-router echarts vue-echarts
```

**3. 项目结构 (Vite + Vue + TS):**

```
frontend/
├── index.html          # Vite 入口 HTML (位于根目录)
├── public/             # 静态资源 (不会被处理)
├── src/
│   ├── assets/         # 项目资源 (会被处理, 如 CSS, 图片)
│   │   └── main.css    # (可选) 全局样式
│   ├── components/     # 可复用 Vue 组件
│   │   ├── PredictionChart.vue
│   │   └── TrainingHistoryChart.vue
│   ├── layouts/        # 页面布局
│   │   └── DefaultLayout.vue
│   ├── pages/          # 页面级组件
│   │   ├── HomePage.vue
│   │   ├── InferencePage.vue
│   │   └── PerformancePage.vue
│   ├── router/         # Vue Router 配置 (index.ts)
│   ├── services/       # API 请求服务 (api.ts)
│   ├── store/          # Pinia 状态管理 (index.ts, modules/*.ts)
│   ├── types/          # TypeScript 类型定义
│   │   └── api.ts      # API 相关类型
│   │   └── index.ts    # 其他类型
│   ├── App.vue         # 根组件
│   └── main.ts         # 应用入口 (引入 Vue, Router, Pinia, Element Plus)
├── package.json
├── tsconfig.json
├── tsconfig.node.json
└── vite.config.ts      # Vite 配置文件 (重要!)
```

**4. 页面设计 (使用 Element Plus 组件):**

* **main.ts** **(入口文件):**

  * **引入** **createApp** **from 'vue'**
  * **引入** **App** **from './App.vue'**
  * **引入** **router** **from './router'**
  * **引入** **pinia** **from './store'**
  * **引入** **ElementPlus** **from 'element-plus'**
  * **引入** **import 'element-plus/dist/index.css'** **(Element Plus 样式)**
  * **引入 ECharts 相关 (如果需要全局注册)**
  * **创建 Vue 应用:** **const app = createApp(App)**
  * **使用插件:** **app.use(pinia)**, **app.use(router)**, **app.use(ElementPlus)**
  * **挂载应用:** **app.mount('#app')**
* **DefaultLayout.vue** **(布局):**

  * **使用** **`<el-container direction="horizontal">`**。
  * **侧边栏:** **`<el-aside width="200px">`** **内含** **`<el-menu :default-active="$route.path" router>`**，包含指向各页面的 **`<el-menu-item>`**。
  * **主区域:** **`<el-container direction="vertical">`** **包含可选的** **`<el-header>`** **和** **`<el-main>`**。**`<el-main>`** **内放置** **`<router-view />`**。
* **HomePage.vue** **(主页面):**

  * **使用** **`<el-card>`** **包裹内容。**
  * **显著展示系统名称，例如使用** **`<h1>`** **或** **`<p style="font-size: 24px; font-weight: bold; text-align: center; margin: 20px 0;">`联邦学习图像识别效果评估平台 `</p>`**。
  * **添加简短的系统介绍文本** **`<p>`本平台用于加载和可视化展示预训练联邦学习模型的图像识别效果。`</p>`**。
* **InferencePage.vue** **(模型效果页面):**

  * **布局:** **可用** **`<el-row :gutter="20">`** **和** **`<el-col :span="10">`** **(左侧控制) 与** **`<el-col :span="14">`** **(右侧结果)。**
  * **左侧控制区 (**`<el-col :span="10">`**):**

    * **使用** **`<el-card header="模型与图像选择">`**。
    * **模型选择:** **`<el-form-item label="选择模型"><el-select v-model="selectedModelId" placeholder="请选择模型">`<el-option v-for="model in availableModels" ... />`</el-select></el-form-item>`**。
    * **图片上传:** **`<el-form-item label="上传图片"><el-upload action="#" :auto-upload="false" :on-change="handleFileChange" list-type="picture-card" :limit="1">``<el-icon><Plus />``</el-icon></el-upload>``</el-form-item>`**。 (需要导入 **Plus** **图标)。预览逻辑在** **handleFileChange** **中处理。**
    * **预测按钮:** **<el-button type="primary" @click="handlePredict" :loading="isLoadingPrediction">开始预测 `</el-button>`**。
  * **右侧结果区 (**`<el-col :span="14">`**):**

    * **使用** **`<el-card header="预测结果">`**。
    * **加载状态:** **`<el-skeleton v-if="isLoadingPrediction" :rows="5" animated />`**。
    * **空状态:** **`<el-empty v-if="!predictionResult && !isLoadingPrediction" description="等待预测"></el-empty>`**。
    * **结果图表:** **`<PredictionChart v-if="predictionResult" :data="predictionResult" />`** **(自定义组件，封装 ECharts 柱状图)。**
    * **错误提示:** **`<el-alert v-if="predictionError" :title="predictionError" type="error" show-icon :closable="false"></el-alert>`**。
* **PerformancePage.vue** **(模型综合效果页面):**

  * **布局:** **可用一个** **`<el-card>`** **放选择器/上传，另一个** **`<el-card>`** **放图表。**
  * **数据源选择区:**

    * **(方案一: 后端管理)** **`<el-form-item label="选择模型">`<el-select v-model="selectedHistoryModelId" @change="loadHistoryData" placeholder="选择模型查看历史"><el-option ... />`</el-select></el-form-item>`**。
    * **(方案二: 用户上传)** **`<el-upload action="#" :auto-upload="false" :on-change="handleHistoryFileChange" :limit="1" accept=".json"><el-button type="success">`上传训练历史文件 (.json)`</el-button></el-upload>`**。
  * **图表展示区 (**`<el-card header="训练过程可视化">`**):**

    * **加载状态:** **`<el-skeleton v-if="isLoadingHistory" :rows="6" animated />`**。
    * **空状态:** **`<el-empty v-if="!trainingHistoryData && !isLoadingHistory" description="请选择模型或上传文件"></el-empty>`**。
    * **图表容器:** **`<div v-if="trainingHistoryData">`**

      * **`<el-row :gutter="20">`**

        * **`<el-col :span="12"><TrainingHistoryChart title="准确率" :rounds="trainingHistoryData.rounds" :values="trainingHistoryData.accuracies" />``</el-col>`**
        * **`<el-col :span="12"><TrainingHistoryChart title="损失" :rounds="trainingHistoryData.rounds" :values="trainingHistoryData.losses" />``</el-col>`**
      * **`</el-row>`**
      * **(可选) 显示总训练时间:** **`<p>`总训练时间: {{ trainingHistoryData.total_training_time }}`</p>`**
    * **错误提示:** **`<el-alert v-if="historyError" :title="historyError" type="error" show-icon :closable="false"></el-alert>`**。

**5. 状态管理 (Pinia -** **src/store/modules/modelStore.ts**):
(与之前设计类似)

* **availableModels**: **Ref<ModelInfo[]>**
* **selectedModelId**: **Ref<number | string | null>**
* **uploadedImageFile**: **Ref<File | null>** **(存储原始文件对象，或处理后的 base64)**
* **predictionResult**: **Ref<Prediction[] | null>**
* **isLoadingPrediction**: **Ref `<boolean>`**
* **predictionError**: **Ref<string | null>**
* **trainingHistoryData**: **Ref<TrainingHistoryData | null>**
* **isLoadingHistory**: **Ref `<boolean>`**
* **historyError**: **Ref<string | null>**
* **Actions:** **fetchAvailableModels**, **runPrediction**, **loadTrainingHistory** **(根据模型 ID 或上传的文件)。**

**6. API 服务 (**src/services/api.ts**):**
(与之前设计类似)

* **使用 Axios 实例。**
* **封装函数：**getModels()**,** **postPrediction(modelId, imageData)**, **getTrainingHistory(modelId)**。
* **定义好请求和响应的 TypeScript 类型 (**src/types/api.ts**)。**

**7. Vite 配置 (**vite.config.ts**):**

* **可能需要配置** **server.proxy** **来解决开发环境下的跨域问题，将** **/api** **请求转发给 Django 后端。**

  ```typescript
  import { defineConfig } from 'vite'
  import vue from '@vitejs/plugin-vue'
  ```
* ```typescript
   export default defineConfig({
     plugins: [vue()],
     server: {
       proxy: {
         // 字符串简写写法
         // '/api': 'http://localhost:8000',
         // 选项写法
         '/api': {
           target: 'http://127.0.0.1:8000', // 后端服务实际地址
           changeOrigin: true, // 需要虚拟主机站点
           // rewrite: (path) => path.replace(/^\/api/, '') // 如果后端接口不带 /api 前缀，需要重写
         }
       }
     }
   })
  ```
* **如果使用 Element Plus 按需导入，需要配置相关插件 (**unplugin-vue-components**,** **unplugin-auto-import**)。

### 第二部分：后端设计 (Python + Django + DRF)

**1. 技术栈:**

* **语言:** **Python 3**
* **框架:** **Django**
* **API 框架:** **Django Rest Framework (DRF)**
* **数据库:** **PostgreSQL / MySQL / SQLite (开发用 SQLite 足够)**
* **模型运行库:**  **PyTorch (根据你的模型选择)**
* **图像处理:** **Pillow**
* **CORS:** **django-cors-headers**

```
backend/
├── manage.py
├── project_name/      # Django 项目配置 (settings.py, urls.py...)
├── api/               # Django App for API logic (models.py, serializers.py, views.py, urls.py...)
│   └── services/      # (可选) 放置模型加载和推理逻辑 (inference_service.py)
├── media/             # 存储模型文件和历史记录 (配置 MEDIA_ROOT)
│   └── models/
│       ├── model_a/
│       │   ├── model.h5 / model.pth
│       │   └── history.json
│       └── ...
├── requirements.txt
└── .env               # (可选) 环境变量
```

**3. 数据库模型 (**api/models.py**):** **(与之前设计相同)**

* **PretrainedModel** **类，包含** **name**, **description**, **framework**, **model_file** **(路径),** **history_file** **(路径),** **class_labels** **(JSON),** **input_shape** **(JSON) 等字段。**
* **重要:** **需要手动将模型文件 (如** **.h5**, **.pth**) 和 **history.json** **文件放到** **media/models/** **下对应的子目录，并在数据库中创建** **PretrainedModel** **记录，填入正确的文件相对路径和类别标签。**

**4. 序列化器 (**api/serializers.py**):** **(与之前设计相同)**

* **BaseModelSerializer**: 用于列表展示模型基本信息 (**id**, **name**, **description**)。
* **PredictionRequestSerializer**: 验证 **/api/predict/** **请求体 (**model_id**,** **image_data** **- base64 字符串)。**
* **PredictionResultSerializer**: 格式化单条预测结果 (**label**, **probability**)。

**5. 视图 (**api/views.py**):** **(与之前设计相同，重点回顾)**

* **ModelListView (generics.ListAPIView)**: 返回所有 **PretrainedModel** **的基本信息列表 (GET** **/api/models/**)。
* **PredictView (views.APIView)**:

  * **接收 POST 请求到** **/api/predict/**。
  * **使用** **PredictionRequestSerializer** **验证输入。**
  * **根据** **model_id** **查找** **PretrainedModel** **记录。**
  * **加载模型:** **(可添加缓存) 调用** **load_model_from_file** **函数，根据** **framework** **加载 TF 或 PyTorch 模型。**
  * **处理图像:** **解码 Base64 图片数据，使用 Pillow 进行打开、转换 (RGB)、缩放 (根据** **input_shape**)。
  * **预处理:** **将图像转为 NumPy 数组，归一化 (需与模型训练时一致)，增加 Batch 维度，可能调整维度顺序 (如 PyTorch 的 NCHW)。**
  * **推理:** **调用** **model.predict()** **(TF) 或** **model(input_tensor)** **(PyTorch)。**
  * **格式化输出:** **将预测概率与** **class_labels** **结合，使用** **PredictionResultSerializer** **序列化成** **[{label: "cat", probability: 0.9}, ...]** **格式，包含在** **{"predictions": [...]}** **中返回。**
  * **错误处理:** **捕获文件未找到、图像处理错误、模型加载/推理错误、标签数量不匹配等异常，返回合适的 HTTP 状态码和错误信息。**
* **TrainingHistoryView (views.APIView)**:

  * **接收 GET 请求到** **/api/models/{model_id}/training_history/**。
  * **根据** **model_id** **查找** **PretrainedModel** **记录，获取** **history_file** **路径。**
  * **读取对应的** **history.json** **文件。**
  * **验证 JSON:** **确保包含** **rounds**, **accuracies**, **losses** **等必要键。**
  * **返回 JSON 文件内容。**
  * **错误处理:** **捕获文件未找到、JSON 解析错误等。**

**6. URL 配置 (**api/urls.py**,** **project_name/urls.py**): **(与之前设计相同)**

* **在** **api/urls.py** **中定义** **/models/**, **/predict/**, **/models/[int:model_id](int:model_id)/training_history/** **路由。**
* **在** **project_name/urls.py** **中** **include('api.urls')** **到** **/api/** **路径下。**

**7. 设置 (**project_name/settings.py**):** **(与之前设计相同)**

* **添加** **'rest_framework'**, **'api'**, **'corsheaders'** **到** **INSTALLED_APPS**。
* **添加** **'corsheaders.middleware.CorsMiddleware'** **到** **MIDDLEWARE** **(通常放在靠前位置)。**
* **配置** **CORS_ALLOWED_ORIGINS** **允许来自 Vite 开发服务器的源 (例如** **http://localhost:5173** **或** **http://127.0.0.1:5173**)。生产环境需要配置前端部署的域名。
* **配置** **MEDIA_URL = '/media/'** **和** **MEDIA_ROOT = os.path.join(BASE_DIR, 'media')**。

### 第三部分：开发与集成

* **启动后端:** **cd backend && python manage.py runserver** **(通常在** **http://127.0.0.1:8000**)。
* **启动前端:** **cd frontend && npm run dev** **(通常在** **http://localhost:5173**)。
* **访问前端:** **在浏览器中打开 Vite 提供的地址。**
* **交互:** **前端页面通过 Axios 向后端 API (**/api/...**) 发送请求。如果配置了 Vite 代理，前端可以直接请求** **/api/...**；否则需要请求完整后端地址 **http://127.0.0.1:8000/api/...** **(并确保 CORS 配置正确)。**
* **调试:** **使用浏览器开发者工具查看网络请求和前端日志，使用 Django/Python 的调试工具查看后端日志和错误。**

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
backend-flask/
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
