-- 创建管理员表
CREATE TABLE IF NOT EXISTS administrators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    full_name VARCHAR(100),
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 添加一个管理员实例（密码应该在实际应用中加密保存）
INSERT INTO administrators (username, password, email, full_name)
VALUES ('admin', 'admin123', 'admin@flimgsys.com', '系统管理员'); 