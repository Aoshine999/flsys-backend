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
