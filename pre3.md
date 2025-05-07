### 1. 实现身份验证API接口

1.1 管理员登录接口* 路径: /api/auth/login

* 方法: POST
* 接收数据: {username, password}

```plaintext
  {
    "admin": {
      "id": 数字,
      "username": "字符串",
      "email": "字符串(可选)",
      "full_name": "字符串(可选)",
      "is_active": 布尔值
    },
    "token": "JWT令牌字符串"
  }
```

* 功能: 验证用户凭据并生成JWT令牌

1.2 管理员登出接口 *  路径: /api/auth/logout

* 方法: POST
* 需要认证: 是
* 返回数据: {"success": true, "message": "退出成功"}
* 功能: 使当前令牌失效

1.3 获取当前管理员信息接口* 路径: /api/auth/me

* 方法: GET
* 需要认证: 是
* 返回数据:

```plaintext
  {
    "admin": {
      "id": 数字,
      "username": "字符串",
      "email": "字符串(可选)",
      "full_name": "字符串(可选)",
      "is_active": 布尔值
    }
  }
```

1.4  用户注册接口

- 接口路径: /api/auth/register

- 请求方法: POST

- Content-Type: application/json

- 请求参数:

```json
{
  "username": "string", // 必填，用户名
  "password": "string", // 必填，密码
  "email": "string",    // 可选，邮箱
  "full_name": "string" // 可选，姓名
}
```



参数验证规则:

- username: 3-20个字符，只允许字母、数字和下划线，必须唯一

* password: 最小长度6位，建议混合字母和数字
* email: 有效的邮箱格式，可选但推荐提供
* full_name: 用户真实姓名，可选

成功响应: (状态码: 200)


```jso
{
  "admin": {
    "id": 123,
    "username": "example_user",
    "email": "user@example.com",
    "full_name": "张三",
    "is_active": true
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
} 
```



错误响应:

1. 用户名已存在 (状态码: 409)

```
{
  "message": "用户名已被使用，请更换其他用户名",
  "error_code": "USERNAME_EXISTS"
}
```



2.数据验证失败 (状态码: 400)

```json
{
  "message": "数据验证失败",
  "errors": {
    "username": ["用户名长度必须在3-20个字符之间"],
    "password": ["密码长度不能小于6位"],
    "email": ["邮箱格式不正确"]
  }
}
```

### 2. 数据库和认证机制

2.1 数据库操作* 基于已有的administrators表实现管理员查询和验证

* 确保密码加密存储
* 验证用户状态(is_active)

2.2 JWT认证机制* 实现JWT令牌的生成和验证

* 处理令牌过期情况
* 实现认证中间件

### 3. 安全措施

* 密码加密存储
* 防范SQL注入攻击
* 限制登录失败尝试次数
* 实现适当的CORS策略
* 添加请求日志记录

### 4. 错误处理和响应

* 实现标准化的错误响应格式
* 处理认证失败、禁用账户等特殊情况
* 返回合适的HTTP状态码
